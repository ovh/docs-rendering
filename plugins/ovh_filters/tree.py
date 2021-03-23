def tree(entity):
    """tree is a filter to build the file tree

    Args:
        entity: the current entity

    Returns:
        A file tree, starting with the highest parent
    """
    root = entity

    # Get the highest available parent
    while hasattr(root, 'parent') and root.parent and root.parent.type == root.type:
        root = root.parent

    # Use it to build the file tree
    return build_tree(root, entity.title)

def build_tree(node, active_title=None):
    items = []

    if not hasattr(node, 'children') or not node.children:
        return {
            'title': node.title,
            'url': node.url,
            'active': True if node.title == active_title else False
        }

    for child in node.children:
        items.append(build_tree(child, active_title))

    return {
        'title': node.title,
        'url': node.url,
        'children': items,
        'active': True if node.title == active_title else False
    }

