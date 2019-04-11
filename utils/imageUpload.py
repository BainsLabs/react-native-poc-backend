import cloudinary.uploader


def imageUpload(img):
    cloudinary.config(api_secret="DcBsVAFf3R1Xtt61jqR9rvj0-AU",
                      api_key="331247561554362",
                      cloud_name="faceapp")
    imape_upload = cloudinary.uploader.upload(f'{img}',
                                              use_filename=1,
                                              unique_filename=1)

    return imape_upload['url']
