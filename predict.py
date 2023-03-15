from object_detection import detect_from_hosted_image

# beemart_images = [
#     "https://bizweb.dktcdn.net/thumb/1024x1024/100/004/714/products/bot-mi-so-13-baker-choice.png?v=1644554364560",
#     "https://bizweb.dktcdn.net/thumb/1024x1024/100/004/714/products/whipping-cream-anchor-1l.png?v=1636680602907",
#     "https://bizweb.dktcdn.net/thumb/1024x1024/100/004/714/products/74105f78435f267462883fb9d5ce7316.jpg?v=1655272893883",
# ]
beemart_images = open("data/beemart_image.txt", "r").read().split("\n")
beemart_images = beemart_images[:1000]

abby_images = [
    "https://abby.vn/wp-content/uploads/2022/09/B0414-1635532706367-3.jpeg",
    "https://abby.vn/wp-content/uploads/2021/06/B0466-1622618446100-600x600.jpeg",
    "https://abby.vn/wp-content/uploads/2020/04/B5226-1587693924998.jpeg",
]

processed_images = detect_from_hosted_image(abby_images, beemart_images, save=True)
print(processed_images)
