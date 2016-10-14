def is_stale(e):
    try:
        # poll the link with an arbitrary call
        e.find_elements_by_id('doesnt-matter') 
        return False
    except StaleElementReferenceException:
        return True