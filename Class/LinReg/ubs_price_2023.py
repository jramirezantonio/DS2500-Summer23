"""
Visualization of USB Thumb-drive prices (2019-2023)
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

capacity = [2,     4,     8,    16,   32,   64,   128,   256,   512,   1024,  2000]
price_2019 = [2.0, 3.0,   4.0,   5.0,  7.0, 10.0,  18.0,  40.0, 100.0,  200.,  400.0]
price_2021 = [2,   2.5,   2.8,   3.2, 4.4,  6.5,  15.0,  29.0,  60.0,   42.0,  54.0]
price_2023 = [2.2,   2.2,   2.5,   2.5, 4.0,  4.4,  5.5,  15.25,  23.0,   26.0,  28.0]

price_dict = {'capacity': capacity,
              'price_2019': price_2019,
              'price_2021': price_2021,
              'price_2023': price_2023}

data = pd.DataFrame(price_dict)

print(data)

ci = 80
sns.regplot(x=data.capacity, y=data.price_2019, ci=ci, label='2019')
sns.regplot(x=data.capacity, y=data.price_2021, ci=ci, label='2021')
sns.regplot(x=data.capacity, y=data.price_2023, ci=ci, label='2023')
plt.xlabel('Capacity (Gb)')
plt.ylabel('USD')
plt.title('USB 3.0 typical thumb-drive prices on Amazon.com')
plt.xscale('log')
plt.legend()
plt.show()
