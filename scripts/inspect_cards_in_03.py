import cv2
import numpy as np

img = cv2.imread('reports/final-review-screenshots/03_final_desktop_catalogue.png')
print("Image dimensions:", img.shape)

# Find where the cards are located in 03_final_desktop_catalogue.png
# Let's inspect rows from 200 to 1100
# The cards in 03_final_desktop_catalogue are at top of page because other sections were display:none!
# Let's crop the 3 cards in the top row:
# Card 1: x: 25 to 452
# Card 2: x: 490 to 917
# Card 3: x: 955 to 1382

# Where do they start vertically?
# Let's find where the media image container is:
for i, (x1, x2) in enumerate([(25, 452), (490, 917), (955, 1382)]):
    card_col = img[:, x1:x2]
    # find y where image starts (a border or background)
    cv2.imwrite(f'card_col_{i}.png', card_col)
    print(f"Card {i} column shape: {card_col.shape}")

# Let's also check if there is an image inside card 0
# The media container is a square of approx 427x427.
# Let's find its y offset:
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Let's look at y from 100 to 700 for x in [50, 400]
sub = img[100:600, 50:400]
cv2.imwrite('card0_media_area.png', sub)
print("card0_media_area min BGR:", sub.min(axis=(0,1)), "max BGR:", sub.max(axis=(0,1)), "mean BGR:", sub.mean(axis=(0,1)))
