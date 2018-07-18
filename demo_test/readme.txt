To launch test use this command

pytest \   # This command run all test in current folder and all subfolders
    test_package.py::TestClassName::test_function name      # allow launch target pest module, class or just a single test
    --allure-severities=critical        # Allow launch only test with target severity
    --allure-feature=critical           # Allow launch only test with target feature
    --alluredir=./report_dir_name/      # Set directory for allure meta data, to create allure report after test launch
    -x, --maxfail=%num_of_fail%         # Stop after first fail or num_of_fail