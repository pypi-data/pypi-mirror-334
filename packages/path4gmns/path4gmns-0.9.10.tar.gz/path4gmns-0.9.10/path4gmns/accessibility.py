import os
import csv
import threading

from .classes import AccessNetwork
from .path import single_source_shortest_path
from .consts import MAX_LABEL_COST, MIN_TIME_BUDGET, \
                    BUDGET_TIME_INTVL, MAX_TIME_BUDGET


__all__ = ['evaluate_accessibility', 'evaluate_equity']


def _get_interval_id(t):
    """ return interval id in predefined time budget intervals

    [0, MIN_TIME_BUDGET],

    (MIN_TIME_BUDGET + (i-1)*BUDGET_TIME_INTVL, MIN_TIME_BUDGET + i*BUDGET_TIME_INTVL]
        where, i is integer and i >= 1
    """
    if t < MIN_TIME_BUDGET:
        return 0

    if ((t-MIN_TIME_BUDGET) % BUDGET_TIME_INTVL) == 0:
        return int((t-MIN_TIME_BUDGET) / BUDGET_TIME_INTVL)

    return int((t-MIN_TIME_BUDGET) / BUDGET_TIME_INTVL) + 1


def _update_min_travel_time(an, at, min_travel_times, time_dependent, demand_period_id):
    an.update_generalized_link_cost(at, time_dependent, demand_period_id)

    at_str = at.get_type_str()
    max_min = 0
    for c in an.get_centroids():
        node_id = c.get_node_id()
        zone_id = c.get_zone_id()
        single_source_shortest_path(an, node_id)
        for c_ in an.get_centroids():
            if c_ == c:
                continue

            node_no = c_.get_node_no()
            to_zone_id = c_.get_zone_id()
            min_tt = an.get_node_label_cost(node_no)
            # this function will dramatically slow down the whole process
            min_dist = an.get_sp_distance(node_no)
            min_travel_times[(zone_id, to_zone_id, at_str)] = min_tt, min_dist

            if min_tt < MAX_LABEL_COST and max_min < min_tt:
                max_min = min_tt

    return max_min


def _output_od_accessibility(min_travel_times, zones, mode, output_dir):
    """ output accessibility for each OD pair (i.e., travel time) """
    with open(output_dir+'/od_accessibility.csv', 'w',  newline='') as f:
        headers = ['o_zone_id', 'd_zone_id', 'accessibility', 'distance', 'geometry']

        writer = csv.writer(f)
        writer.writerow(headers)

        # for multimodal case, find the minimum travel time
        # under mode 'a' (i.e., auto)
        for k, v in min_travel_times.items():
            # k = (from_zone_id, to_zone_id, at_type_str)
            if k[2] != mode:
                continue

            # output accessibility
            # no exception handlings here as min_travel_times is constructed
            # directly using an.get_centroids()
            coord_oz = zones[k[0]].get_coordinate_str()
            coord_dz = zones[k[1]].get_coordinate_str()
            geo = 'LINESTRING ()'
            if coord_oz and coord_dz:
                geo = 'LINESTRING (' + coord_oz + ', ' + coord_dz + ')'

            tt = v[0]
            dis = v[1]
            if tt >= MAX_LABEL_COST:
                tt = 'N/A'
                dis = 'N/A'

            line = [k[0], k[1], tt, dis, geo]
            writer.writerow(line)

        if output_dir == '.':
            print(f'check od_accessibility.csv in {os.getcwd()} for OD accessibility')
        else:
            print(
                f'check od_accessibility.csv in {os.path.join(os.getcwd(), output_dir)}'
                ' for OD accessibility'
            )


def _output_zone_accessibility(min_travel_times, interval_num,
                               zones, ats, output_dir):
    """ output zone accessibility matrix for each agent type """

    with open(output_dir+'/zone_accessibility.csv', 'w',  newline='') as f:
        time_budgets = [
            'TT_'+str(MIN_TIME_BUDGET+BUDGET_TIME_INTVL*i) for i in range(interval_num)
        ]

        headers = ['zone_id', 'geometry', 'mode']
        headers.extend(time_budgets)

        writer = csv.writer(f)
        writer.writerow(headers)

        # calculate accessibility
        for oz, v in zones.items():
            if not oz:
                continue

            for at in ats:
                at_str = at.get_type_str()
                # number of accessible zones from oz for each agent type
                counts = [0] * interval_num
                for dz in zones:
                    if (oz, dz, at_str) not in min_travel_times:
                        continue

                    min_tt = min_travel_times[(oz, dz, at_str)][0]
                    if min_tt >= MAX_LABEL_COST:
                        continue

                    id = _get_interval_id(min_tt)
                    while id < interval_num:
                        counts[id] += 1
                        id += 1
                # output accessibility

                # output the zone coordinates rather than the boundaries for the
                # following two reasons:
                # 1. to be consistent with _output_od_accessibility()
                # 2. v.get_geo() is always empty as no boundary info is provided
                #    in node.csv
                geo = 'LINESTRING ()'
                coord = v.get_coordinate_str()
                if coord:
                    geo = 'LINESTRING (' + coord + ')'

                line = [oz, geo, at.get_type_str()]
                line.extend(counts)
                writer.writerow(line)

        if output_dir == '.':
            print(f'check zone_accessibility.csv in {os.getcwd()} for zone accessibility')
        else:
            print(
                f'check zone_accessibility.csv in {os.path.join(os.getcwd(), output_dir)}'
                ' for zone accessibility'
            )


def _output_equity(output_dir, time_budget, equity_metrics, equity_zones):
    with open(output_dir+'/equity_'+str(time_budget)+'min.csv', 'w',  newline='') as f:
        headers = ['bin_index', 'mode', 'zones',
                   'min_accessibility', 'zone_id',
                   'max_accessibility', 'zone_id',
                   'mean_accessibility']
        writer = csv.writer(f)
        writer.writerow(headers)

        for k, v in sorted(equity_metrics.items()):
            try:
                avg = round(v[4] / len(equity_zones[k]), 2)
                zones = ', '.join(str(x) for x in equity_zones[k])
                line = [k[0], k[1], zones, v[0], v[1], v[2], v[3], avg]
            except ZeroDivisionError:
                continue

            writer.writerow(line)

        if output_dir == '.':
            print(
                f'\ncheck equity_{time_budget} min.csv in {os.getcwd()} for equity evaluation')
        else:
            print(
                f'\ncheck equity_{time_budget} min.csv in {os.path.join(os.getcwd(), output_dir)}'
                ' for equity evaluation')


def evaluate_accessibility(ui,
                           single_mode=False,
                           mode='auto',
                           time_dependent=False,
                           demand_period_id=0,
                           output_dir='.'):
    """ perform accessibility evaluation for a target mode or more

    Parameters
    ----------
    ui
        network object generated by pg.read_network()

    single_mode
        True or False. Its default value is False. It will only affect the
        output to zone_accessibility.csv.

        If False, the accessibility evaluation will be conducted
        for all the modes defined in settings.yml. The number of accessible
        zones from each zone under each defined mode given a budget time (up
        to 240 minutes) will be outputted to zone_accessibility.csv.

        If True, the accessibility evaluation will be only conducted against the
        target mode. The number of accessible zones from each zone under the
        target mode given a budget time (up to 240 minutes) will be outputted
        to zone_accessibility.csv.

    mode
        target mode with its default value as 'auto'. It can be
        either agent type or its name. For example, 'w' and 'walk' are
        equivalent inputs.

    time_dependent
        True or False. Its default value is False.

        If True, the accessibility will be evaluated using the period link
        free-flow travel time (i.e., VDF_fftt). In other words, the
        accessibility is time-dependent.

        If False, the accessibility will be evaluated using the link length and
        the free flow travel speed of each mode.

    demand_period_id
        The sequence number of demand period listed in demand_periods in
        settings.yml. demand_period_id of the first demand_period is 0.

        Use it with time_dependent when there are multiple demand periods. Its
        default value is 0.

    output_dir
        The directory path where zone_accessibility.csv and od_accessibility.csv
        are output. The default is the current working directory (CDW).

    Returns
    -------
    None

    Note
    ----
    The following files will be output.

    zone_accessibility.csv
        accessibility as the number of accessible zones from each
        zone for a target mode or any mode defined in settings.yml given a
        budget time (up to 240 minutes).

    od_accessibility.csv:
        accessibility between each OD pair in terms of free flow travel time.
    """
    base = ui._base_assignment
    an = AccessNetwork(base.network)
    ats = None

    zones = base.network.zones

    max_min = 0
    min_travel_times = {}
    at_name, at_str = base._convert_mode(mode)
    if not single_mode:
        ats = base.get_agent_types()
        for at in ats:
            an.set_target_mode(at.get_name())
            max_min_ = _update_min_travel_time(an,
                                               at,
                                               min_travel_times,
                                               time_dependent,
                                               demand_period_id)
            if max_min_ > max_min:
                max_min = max_min_
    else:
        an.set_target_mode(at_name)
        at = base.get_agent_type(at_str)
        max_min = _update_min_travel_time(an,
                                          at,
                                          min_travel_times,
                                          time_dependent,
                                          demand_period_id)
        ats = [at]

    interval_num = _get_interval_id(min(max_min, MAX_TIME_BUDGET)) + 1

    # multithreading to reduce output time
    t = threading.Thread(
        target=_output_od_accessibility,
        args=(min_travel_times, zones, at_str, output_dir)
    )
    t.start()

    t = threading.Thread(
        target=_output_zone_accessibility,
        args=(min_travel_times, interval_num, zones, ats, output_dir)
    )
    t.start()


def evaluate_equity(ui, single_mode=False, mode='auto', time_dependent=False,
                    demand_period_id=0, time_budget=60, output_dir='.'):
    """ evaluate equity for each zone under a time budget

    Parameters
    ----------
    ui
        network object generated by pg.read_network()

    single_mode
        True or False. Its default value is False. It will only affect the
        output to zone_accessibility.csv.

        If False, the equity evaluation will be conducted for all the modes defined
        in settings.yml.

        If True, the equity evaluation will be only conducted against the
        target mode.

    mode
        target mode with its default value as 'auto'. It can be
        either agent type or its name. For example, 'w' and 'walk' are
        equivalent inputs.

    time_dependent
        True or False. Its default value is False.

        If True, the accessibility will be evaluated using the period link
        free-flow travel time (i.e., VDF_fftt). In other words, the
        accessibility is time-dependent.

        If False, the accessibility will be evaluated using the link length and
        the free flow travel speed of each mode.

    demand_period_id
        The sequence number of demand period listed in demand_periods in
        settings.yml. demand_period_id of the first demand_period is 0.

        Use it with time_dependent when there are multiple demand periods. Its
        default value is 0.

    time_budget
        the amount of time to travel in minutes

    output_dir
        The directory path where the evaluation result is output. The default
        is the current working directory (CDW).

    Returns
    -------
    None

    Note
    ----
    The following file will be output.

    equity_str.csv
        equity statistics including minimum accessibility (and the corresponding
        zone), maximum accessibility (and the corresponding zone), and mean
        accessibility for each bin_index. The accessible zones will be output
        as well.

        str in the file name refers to the time budget. For example, the file
        name will be equity_60min.csv if the time budget is 60 min.
    """
    base = ui._base_assignment
    an = AccessNetwork(base.network)
    zones = an.base.zones
    ats = None

    min_travel_times = {}
    equity_metrics = {}
    equity_zones = {}

    if not single_mode:
        ats = base.get_agent_types()
        for at in ats:
            an.set_target_mode(at.get_name())
            _update_min_travel_time(an,
                                    at,
                                    min_travel_times,
                                    time_dependent,
                                    demand_period_id)
    else:
        at_name, at_str = base._convert_mode(mode)
        an.set_target_mode(at_name)
        at = base.get_agent_type(at_str)
        _update_min_travel_time(an,
                                at,
                                min_travel_times,
                                time_dependent,
                                demand_period_id)
        ats = [at]

    # v is zone object
    for oz, v in zones.items():
        if not oz:
            continue

        bin_index = v.get_bin_index()
        for at in ats:
            at_str = at.get_type_str()

            count = 0
            for dz in zones:
                if (oz, dz, at_str) not in min_travel_times:
                    continue

                min_tt = min_travel_times[(oz, dz, at_str)][0]
                if min_tt > time_budget:
                    continue

                count += 1

            if (bin_index, at_str) not in equity_metrics:
                equity_metrics[(bin_index, at_str)] = [count, oz, count, oz, 0]
                equity_zones[(bin_index, at_str)] = []
            equity_zones[(bin_index, at_str)].append(oz)

            # 0: min_accessibility, 1: zone_id, 2: max_accessibility,
            # 3: zone_id, 4: cumulative count,
            # where 0 to 4 are indices of each element of equity_metrics.
            if count < equity_metrics[(bin_index, at_str)][0]:
                equity_metrics[(bin_index, at_str)][0] = count
                equity_metrics[(bin_index, at_str)][1] = oz
            elif count > equity_metrics[(bin_index, at_str)][2]:
                equity_metrics[(bin_index, at_str)][2] = count
                equity_metrics[(bin_index, at_str)][3] = oz

            equity_metrics[(bin_index, at_str)][4] += count

    _output_equity(output_dir, time_budget, equity_metrics, equity_zones)