import sys
from robots.robot_demo.main import run as run_demo

ROBOTS = {
    "demo": run_demo,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python run_robot.py demo")
        sys.exit(1)

    robot_name = sys.argv[1]

    if robot_name not in ROBOTS:
        print(f"Robot inconnu : {robot_name}")
        sys.exit(1)

    ROBOTS[robot_name]()