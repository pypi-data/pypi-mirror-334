import grid2op
from pandamodelsbackend import PandaModelsBackend
import pandapower as pp
import pandapower.converter as pp_converter
import os
import numpy as np

def test_grid2op_pandapower():
    """
    Full test for Grid2Op with PandaPower backend.
    - Lists available Grid2Op test environments.
    - Loads an environment and converts its network to PandaPower.
    - Runs a basic simulation with a dummy action.
    - Ensures the backend works without errors.
    """

    # Step 1: List available test environments
    available_envs = grid2op.list_available_test_env()
    if not available_envs:
        print("❌ No available Grid2Op test environments found!")
        return
    print(f"✅ Found {len(available_envs)} available Grid2Op test environments.")

    # Step 2: Pick the first available test environment
    env_name = available_envs[2]
    print(f"✅ Running test on Grid2Op environment: {env_name}")

    # Step 3: Construct the test environment path
    path_grid2op = os.path.dirname(grid2op.__file__)
    path_data_test = os.path.join(path_grid2op, "data", env_name)

    # Step 4: Find a valid grid file
    possible_files = ["grid.json", "case.m", "grid.m"]
    network_file = None

    for file in possible_files:
        full_path = os.path.join(path_data_test, file)
        if os.path.exists(full_path):
            network_file = full_path
            break

    if not network_file:
        print(f"❌ No valid grid file found in {path_data_test}")
        return

    print(f"✅ Found network file: {network_file}")

    # Step 5: Convert the environment grid to a PandaPower network
    try:
        if network_file.endswith(".json"):
            pp_net = pp.from_json(network_file)  # Load PandaPower JSON
            print("✅ Loaded grid from JSON")
        else:
            pp_net = pp_converter.from_mpc(network_file, f_hz=50)  # Convert MATPOWER to PandaPower
            print("✅ Converted MATPOWER to PandaPower network")
    except Exception as e:
        print(f"❌ Error loading grid file: {e}")
        return

    # Step 6: Initialize Grid2Op with the PandaPower backend
    backend = PandaModelsBackend(pp_net)
    env = grid2op.make(env_name, backend=backend)  # Fix missing dataset argument

    # Step 7: Reset the environment
    obs = env.reset()

    # Step 8: Take a simple action (do nothing)
    action = env.action_space()
    obs, reward, done, info = env.step(action)

    # Step 9: Validate results
    assert not done, "❌ Simulation ended too early!"
    assert not np.isnan(obs.rho.max()), "❌ Invalid line loading (NaN detected)!"
    assert not np.isnan(obs.prod_p.max()), "❌ Invalid generator production (NaN detected)!"

    print("✅ Grid2Op PandaPower Backend Test Passed: Environment runs successfully!")

# Run the test
if __name__ == "__main__":
    test_grid2op_pandapower()
