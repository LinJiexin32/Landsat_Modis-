import ee
ee.Initialize()
for i in range(0,9):
    name = 'users/2018302060260/ndvi_landsat8/ndvi' + str(i)
    ee.data.deleteAsset(name)
    print(name)

