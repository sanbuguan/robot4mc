#!/usr/bin/env python
# -*- coding: utf-8 -*-

class url_config:
    #url login post
    url_login="https://meican.com/account/directlogin"

#url get left tab
    tab_url='https://meican.com/preorder/api/v2.1/calendarItems/list?beginDate=%s&endDate=%s&noHttpGetCache=1532574727555&withOrderDetail=false'

#url get restrants
    restrants_url='https://meican.com/preorder/api/v2.1/restaurants/list?tabUniqueId=%s&targetTime=%s+17:00'

#url get dinnerlist
    dinner_url='https://meican.com/preorder/api/v2.1/restaurants/show?restaurantUniqueId=%s&tabUniqueId=%s&targetTime=%s+17:00'

#url order dinner
    order_dinner_url='https://meican.com/preorder/api/v2.1/orders/add?corpAddressRemark=&corpAddressUniqueId=%s&order'+ \
                     '=[{"count":1,"dishId":%s}]&remarks=null&tabUniqueId=%s&targetTime=%s+17:00&userAddressUniqueId=%s'

#url query dinner
    query_url='https://meican.com/preorder/api/v2.1/calendaritems/list?withOrderDetail=false&beginDate=%s&endDate=%s'
    order_info_url='https://meican.com/preorder/api/v2.1/orders/show'




