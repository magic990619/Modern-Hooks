from django import template

register = template.Library()


@register.inclusion_tag('candidate_detail_view.html')
def average_rating_stars(rate):
    rating = rate
    n = 5
    responce = []
    while n > 0:
        n -= 1
        if rating > 0:
            if rating > 0.5:
                rating -= 1
                responce.append("fa fa-star")
            else:
                rating -= 0.5
                responce.append("fa fa-star-half-full")
        else:
            responce.append("fa fa-star-o")
    return responce


register.filter('average_rating_stars', average_rating_stars)
