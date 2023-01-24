def build():
    print("Building...")

def test():
    print("Testing...")

def deploy():
    print("Deploying...")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Please provide a function name")
    else:
        func_name = sys.argv[1]
        if func_name == "build":
            build()
        elif func_name == "test":
            test()
        elif func_name == "deploy":
            deploy()
        else:
            print(f"{func_name} is not a valid function name")
