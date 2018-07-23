from allure import step

from ui import main_page, item_page


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
