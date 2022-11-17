import time
import datetime
import sys
from reconstruction.make_fragments import run as make_fragments
from reconstruction.register_fragments import run as register_fragments
from reconstruction.refine_registration import run as refine_registration
from reconstruction.integrate_scene import run as integrate_scene
from reconstruction.slac_integrate import run as slac_integrate
from reconstruction.initialize_config import initialize_config


def pipeline(slac=False, debug=False):
    config = {"debug_mode": debug}

    initialize_config(config)

    times = []
    start_time = time.time()
    make_fragments(config)
    times.append(time.time() - start_time)

    start_time = time.time()
    register_fragments(config)
    times.append(time.time() - start_time)

    start_time = time.time()
    refine_registration(config)
    times.append(time.time() - start_time)

    start_time = time.time()
    integrate_scene(config)
    times.append(time.time() - start_time)

    if slac:
        start_time = time.time()
        slac(config)
        times.append(time.time() - start_time)
        start_time = time.time()
        slac_integrate(config)
        times.append(time.time() - start_time)

    print("====================================")
    print("Elapsed time (in h:m:s)")
    print("====================================")
    print("- Making fragments    %s" % datetime.timedelta(seconds=times[0]))
    print("- Register fragments  %s" % datetime.timedelta(seconds=times[1]))
    print("- Refine registration %s" % datetime.timedelta(seconds=times[2]))
    print("- Integrate frames    %s" % datetime.timedelta(seconds=times[3]))
    print("- SLAC                %s" % datetime.timedelta(seconds=times[4]))
    print("- SLAC Integrate      %s" % datetime.timedelta(seconds=times[5]))
    print("- Total               %s" % datetime.timedelta(seconds=sum(times)))
    sys.stdout.flush()
