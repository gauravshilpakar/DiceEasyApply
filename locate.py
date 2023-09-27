def locate_element(list_container, driver):
    container = None
    for x in list_container:
        try:
            container = driver.find_element(By.XPATH, x)
            if container.is_enabled():
                print(x)
                return container
        except:
            ...
