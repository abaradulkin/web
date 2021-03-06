from allure import step

from ui import main_page, item_page, delivery_page, lti_page, testtaker_page, test_creation_page


@step("Add interaction to item")
def add_interaction_to_item(item_obj, choice=None):
    main_page.open_items()
    item_page.open_target_item(item_obj.label)
    item_page.open_authoring()
    item_page.authoring_actions.add_choice()  # TODO: add different types of interaction
    if choice:  # TODO: make choise as part of item_obj
        item_page.authoring_actions.select_correct_choice(choice)
        item_page.authoring_actions.check_choice_selected(choice)
    item_page.authoring_actions.save_items()
    item_page.check_popup_message("Your item has been saved")


@step("Create new delivery")
def create_new_delivery(delivery_obj):
    main_page.open_delivery()
    delivery_page.start_creation_new_delivery()
    assert delivery_obj.test, "Delivery {} should contains test obj to be created".format(delivery_obj.label)
    delivery_page.select_test_for_delivery(delivery_obj.test)
    delivery_page.check_popup_message("Publishing of \"{}\" completed".format(delivery_obj.test.label))
    delivery_page.set_name_and_save(delivery_obj.label)
    delivery_page.check_popup_message("Delivery saved")
    if delivery_obj.group:
        delivery_page.select_group_for_delivery(delivery_obj.group)
        delivery_page.check_popup_message("Selection saved successfully")


@step("Create new item")
def create_new_item(item_obj):
    main_page.open_items()
    item_page.start_creation_new_item()
    item_page.set_name_and_save(label=item_obj.label, popup_msg="Item saved")
    item_page.wait_page_reloaded()


@step("Create new testtaker")
def create_new_testtaker(testtaker_obj):
    main_page.open_test_takers()
    testtaker_page.start_testtaker_creation()

    testtaker_page.select_language(testtaker_obj.language)
    testtaker_page.fill_login(testtaker_obj.login)
    testtaker_page.fill_label(testtaker_obj.label)
    testtaker_page.fill_password(testtaker_obj.password)

    testtaker_page.save_current_object()
    testtaker_page.check_popup_message("Test-taker saved")


@step("Create new test with selected items")
def create_new_test(test_obj, item_list):
    main_page.open_tests()
    test_creation_page.create_new_test(test_obj.label)
    test_creation_page.open_test_authoring(test_obj.label)
    for item in item_list:
        test_creation_page.authoring_actions.select_item(item)
    test_creation_page.authoring_actions.add_selected_items()
    test_creation_page.authoring_actions.save()
    test_creation_page.check_popup_message("Test Saved")


@step("Create new LTI")
def create_new_lti(lti_obj):
    main_page.open_settings()
    main_page.open_lti_tab()
    lti_page.start_lti_creation()
    lti_page.fill_lti_label(lti_obj.label)
    if lti_obj.key:
        lti_page.fill_lti_key(lti_obj.key)
    if lti_obj.secret:
        lti_page.fill_lti_secret(lti_obj.secret)
    lti_page.finish_creation_action()
    lti_page.check_popup_message("{} created".format(lti_obj.label))


@step("Create new user")
def create_new_user(user_obj):
    main_page.open_users()
    main_page.open_add_user_tab()

    # TODO: merge this method with create_new_testtaker()
    testtaker_page.select_language(user_obj.language)
    testtaker_page.fill_login(user_obj.login)
    testtaker_page.fill_label(user_obj.label)
    testtaker_page.fill_password(user_obj.password)
    testtaker_page.fill_role(user_obj.role)

    testtaker_page.save_current_object()
    testtaker_page.check_popup_message("User added")


@step("Delete target item")
def delete_target_item(item_obj):
    main_page.open_items()
    item_page.open_target_item(item_obj.label)
    item_page.make_deletion_action()
    item_page.wait_page_reloaded()


@step("Remove interaction from target item")
def remove_interaction_from_item(item_obj):
    main_page.open_items()
    item_page.open_target_item(item_obj.label)
    item_page.open_authoring()
    item_page.authoring_actions.remove_choice()
    item_page.authoring_actions.save_items()
    item_page.check_popup_message("Your item has been saved")


@step("Rename target item")
def rename_item(old_item_name, new_item_name):
    main_page.open_items()
    item_page.open_target_item(old_item_name)
    item_page.set_name_and_save(new_item_name)
    item_page.check_popup_message("Item saved")
