import untangle
import argparse

def get_stock(product_id, store_id=None, region='us/en'):
    url = 'http://www.ikea.com/%s/iows/catalog/availability/%s'
    doc = untangle.parse(url % (region, product_id))
    stores = doc.ir_ikea_rest.availability.localStore
    if store_id:
        return filter(lambda x: int(x['buCode']) == int(store_id), stores)[0]
    else:
        return stores

def store_info(store_element):
    info = {}
    info['store_id'] = int(store_element['buCode'])
    info['sold_in_store'] = store_element.stock.isSoldInStore.cdata
    info['in_stock'] = store_element.stock.inStockProbabilityCode.cdata
    info['available_stock'] = int(store_element.stock.availableStock.cdata)
    try:
        info['restock_date'] = store_element.stock.restockDate.cdata
    except IndexError:
        pass
    return info

def print_info(info):
    print "Store %(store_id)d: %(available_stock)d in stock" % info
    if 'restock_date' in info:
        print "    Restock date: %(restock_date)s" % info

def main():
    parser = argparse.ArgumentParser(description='Check stock of products at IKEA stores', add_help=True)
    parser.add_argument('product_id', action='store', help='ID of product to check stock of')
    parser.add_argument('-s', action='store', dest='store_id', help='ID of store to check stock at')
    parser.add_argument('-r', action='store', dest='region', help='Region of IKEA stores to check inventory of (the region/language code following "www.ikea.com" in the URL for your local IKEA site, such as "us/en")', default='us/en')
    args = parser.parse_args()

    stock = get_stock(args.product_id, args.store_id, args.region)
    if args.store_id:
        print_info(store_info(stock))
    else:
        for store in stock:
            print_info(store_info(store))

if __name__ == '__main__':
    main()
