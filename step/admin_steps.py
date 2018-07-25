from allure import step

from ui import main_page, item_page, delivery_page


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

@step("Delete target item")
def delete_target_item(item_obj):
    main_page.open_items()
    item_page.open_target_item(item_obj)
    item_page.make_deletion_action()
    item_page.wait_page_reloaded()


@step("Rename target item")
def rename_item(old_item_name, new_item_name):
    main_page.open_items()
    item_page.open_target_item(old_item_name)
    item_page.set_name_and_save(new_item_name)
    item_page.check_popup_message("Item saved")
