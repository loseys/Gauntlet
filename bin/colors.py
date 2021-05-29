class Colors:
    invisible = (255, 0, 128)  # Transparency color.
    red = (255, 0, 0)
    yellow = (255, 255, 100)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    silver = (192, 192, 192)
    select = red


class StatusColor:
    menu_arrows = Colors.green
    page_0_option_0 = Colors.green
    page_0_option_1 = Colors.green
    page_0_option_2 = Colors.green
    page_0_option_3 = Colors.green
    page_0_option_4 = Colors.green
    page_0_option_5 = Colors.green
    page_1_option_0 = Colors.green
    page_1_option_1 = Colors.green
    page_1_option_2 = Colors.green
    page_1_option_3 = Colors.green
    page_1_option_4 = Colors.green
    page_1_option_5 = Colors.green
    page_2_option_0 = Colors.green
    page_2_option_1 = Colors.green
    page_2_option_2 = Colors.green
    page_2_option_3 = Colors.green
    page_2_option_4 = Colors.green
    page_2_option_5 = Colors.green
    page_3_option_0 = Colors.green
    page_3_option_1 = Colors.green
    page_3_option_2 = Colors.green
    page_3_option_3 = Colors.green
    page_3_option_4 = Colors.green
    page_3_option_5 = Colors.green


class SnapShot:
    menu_arrows = Colors.green
    page_0_option_0 = Colors.green
    page_0_option_1 = Colors.green
    page_0_option_2 = Colors.green
    page_0_option_3 = Colors.green
    page_0_option_4 = Colors.green
    page_0_option_5 = Colors.green
    page_1_option_0 = Colors.green
    page_1_option_1 = Colors.green
    page_1_option_2 = Colors.green
    page_1_option_3 = Colors.green
    page_1_option_4 = Colors.green
    page_1_option_5 = Colors.green
    page_2_option_0 = Colors.green
    page_2_option_1 = Colors.green
    page_2_option_2 = Colors.green
    page_2_option_3 = Colors.green
    page_2_option_4 = Colors.green
    page_2_option_5 = Colors.green
    page_3_option_0 = Colors.green
    page_3_option_1 = Colors.green
    page_3_option_2 = Colors.green
    page_3_option_3 = Colors.green
    page_3_option_4 = Colors.green
    page_3_option_5 = Colors.green


def hide_menu():
    StatusColor.menu_arrows = Colors.invisible
    StatusColor.page_0_option_0 = Colors.invisible  # F3
    StatusColor.page_0_option_1 = Colors.invisible  # F4
    StatusColor.page_0_option_2 = Colors.invisible  # F5
    StatusColor.page_0_option_3 = Colors.invisible  # F6
    StatusColor.page_0_option_4 = Colors.invisible  # F8
    StatusColor.page_0_option_5 = Colors.invisible  # F9
    StatusColor.page_1_option_0 = Colors.invisible
    StatusColor.page_1_option_1 = Colors.invisible
    StatusColor.page_1_option_2 = Colors.invisible
    StatusColor.page_1_option_3 = Colors.invisible
    StatusColor.page_1_option_4 = Colors.invisible
    StatusColor.page_1_option_5 = Colors.invisible
    StatusColor.page_2_option_0 = Colors.invisible
    StatusColor.page_2_option_1 = Colors.invisible
    StatusColor.page_2_option_2 = Colors.invisible
    StatusColor.page_2_option_3 = Colors.invisible
    StatusColor.page_2_option_4 = Colors.invisible
    StatusColor.page_2_option_5 = Colors.invisible
    StatusColor.page_3_option_0 = Colors.invisible
    StatusColor.page_3_option_1 = Colors.invisible
    StatusColor.page_3_option_2 = Colors.invisible
    StatusColor.page_3_option_3 = Colors.invisible
    StatusColor.page_3_option_4 = Colors.invisible
    StatusColor.page_3_option_5 = Colors.invisible


def unhide_menu():
    if SnapShot.menu_arrows == Colors.green:
        StatusColor.menu_arrows = Colors.green
    else:
        StatusColor.menu_arrows = Colors.select

    if SnapShot.page_0_option_0 == Colors.green:
        StatusColor.page_0_option_0 = Colors.green
    else:
        StatusColor.page_0_option_0 = Colors.select

    if SnapShot.page_0_option_1 == Colors.green:
        StatusColor.page_0_option_1 = Colors.green
    else:
        StatusColor.page_0_option_1 = Colors.select

    if SnapShot.page_0_option_2 == Colors.green:
        StatusColor.page_0_option_2 = Colors.green
    else:
        StatusColor.page_0_option_2 = Colors.select

    if SnapShot.page_0_option_3 == Colors.green:
        StatusColor.page_0_option_3 = Colors.green
    else:
        StatusColor.page_0_option_3 = Colors.select

    if SnapShot.page_0_option_4 == Colors.green:
        StatusColor.page_0_option_4 = Colors.green
    else:
        StatusColor.page_0_option_4 = Colors.select

    if SnapShot.page_0_option_5 == Colors.green:
        StatusColor.page_0_option_5 = Colors.green
    else:
        StatusColor.page_0_option_5 = Colors.select

    if SnapShot.page_1_option_0 == Colors.green:
        StatusColor.page_1_option_0 = Colors.green
    else:
        StatusColor.page_1_option_0 = Colors.select

    if SnapShot.page_1_option_1 == Colors.green:
        StatusColor.page_1_option_1 = Colors.green
    else:
        StatusColor.page_1_option_1 = Colors.select

    if SnapShot.page_1_option_2 == Colors.green:
        StatusColor.page_1_option_2 = Colors.green
    else:
        StatusColor.page_1_option_2 = Colors.select

    if SnapShot.page_1_option_3 == Colors.green:
        StatusColor.page_1_option_3 = Colors.green
    else:
        StatusColor.page_1_option_3 = Colors.select

    if SnapShot.page_1_option_4 == Colors.green:
        StatusColor.page_1_option_4 = Colors.green
    else:
        StatusColor.page_1_option_4 = Colors.select

    if SnapShot.page_1_option_5 == Colors.green:
        StatusColor.page_1_option_5 = Colors.green
    else:
        StatusColor.page_1_option_5 = Colors.select

    if SnapShot.page_2_option_0 == Colors.green:
        StatusColor.page_2_option_0 = Colors.green
    else:
        StatusColor.page_2_option_0 = Colors.select

    if SnapShot.page_2_option_1 == Colors.green:
        StatusColor.page_2_option_1 = Colors.green
    else:
        StatusColor.page_2_option_1 = Colors.select

    if SnapShot.page_2_option_2 == Colors.green:
        StatusColor.page_2_option_2 = Colors.green
    else:
        StatusColor.page_2_option_2 = Colors.select

    if SnapShot.page_2_option_3 == Colors.green:
        StatusColor.page_2_option_3 = Colors.green
    else:
        StatusColor.page_2_option_3 = Colors.select

    if SnapShot.page_2_option_4 == Colors.green:
        StatusColor.page_2_option_4 = Colors.green
    else:
        StatusColor.page_2_option_4 = Colors.select

    if SnapShot.page_2_option_5 == Colors.green:
        StatusColor.page_2_option_5 = Colors.green
    else:
        StatusColor.page_2_option_5 = Colors.select

    if SnapShot.page_3_option_0 == Colors.green:  # ESP
        StatusColor.page_3_option_0 = Colors.green
    else:
        StatusColor.page_3_option_0 = Colors.select

    if SnapShot.page_3_option_1 == Colors.green:
        StatusColor.page_3_option_1 = Colors.green
    else:
        StatusColor.page_3_option_1 = Colors.select

    if SnapShot.page_3_option_2 == Colors.green:
        StatusColor.page_3_option_2 = Colors.green
    else:
        StatusColor.page_3_option_2 = Colors.select

    if SnapShot.page_3_option_3 == Colors.green:
        StatusColor.page_3_option_3 = Colors.green
    else:
        StatusColor.page_3_option_3 = Colors.select

    if SnapShot.page_3_option_4 == Colors.green:
        StatusColor.page_3_option_4 = Colors.green
    else:
        StatusColor.page_3_option_4 = Colors.select

    if SnapShot.page_3_option_5 == Colors.green:
        StatusColor.page_3_option_5 = Colors.green
    else:
        StatusColor.page_3_option_5 = Colors.select
