def get_children(qs_children):
    res = []
    for comment in qs_children:
        c = {
            'id': comment.id,
            'user_id': comment.user.id,
            'text': comment.text,
            'published': comment.published.strftime('%Y-%m-%d %H:%m'),
            'parent_id': comment.get_parent,
            'is_child': comment.is_child,
        }
        if comment.children_comments:
            c['children'] = get_children(comment.children_comments.all())
        res.append(c)
    return res


def create_comments_tree(queryset):
    res = []
    for comment in queryset:
        c = {
            'id': comment.id,
            'user_id': comment.user.id,
            'text': comment.text,
            'published': comment.published.strftime('%Y-%m-%d %H:%m'),
            'parent_id': comment.get_parent,
            'is_child': comment.is_child,
        }
        if comment.children_comments:
            c['children'] = get_children(comment.children_comments.all())
        if not comment.is_child:
            res.append(c)
    return res