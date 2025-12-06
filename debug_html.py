from bs4 import BeautifulSoup

# Load HTML
with open('temp_mark1.html', 'rb') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# Find all p tags
all_p = soup.find_all('p')
print(f'Total p tags: {len(all_p)}')

# Look for verse-like content
for i, p in enumerate(all_p[:20]):
    classes = p.get('class', [])
    id_attr = p.get('id', '')
    text = p.get_text()[:80]
    print(f"{i}: class={classes}, id={id_attr}, text={text}")
