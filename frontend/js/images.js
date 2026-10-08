/*
 * FIND YOUR REAL FRIEND — COMPLETE PHOTO MAP
 * Every quiz option gets a visual photo source.
 * Exact products/games use dedicated images where available.
 * All other options use a relevant photo-search query.
 */
const EXACT_PHOTOS = {
  "Dairy Milk":"https://images.cdn.dunnesstoresgrocery.com/detail/100810627_1.jpg",
  "KitKat":"https://commons.wikimedia.org/wiki/Special:Redirect/file/Kit_kat.jpg",
  "5 Star":"https://img.clevup.in/330294/Cadbury-5-Star-Chocolate-Bar-10-1759509474404.jpeg?format=webp",
  "Perk":"https://wholesaler.pk/image/catalog/Cadbury-Perk-Chocolate-9-8g-Local.jpg",
  "Munch":"https://assets.winni.in/c_limit%2Cdpr_1%2Cfl_progressive%2Cq_80%2Cw_1000/27519_1-munch.jpeg",
  "Ferrero Rocher":"https://images-cdn.ubuy.co.in/69997672044feb4853079761-ferrero-rocher-fine-hazelnut-chocolate.jpg",
  "Snickers":"https://elsuper.com.co/rails/active_storage/representations/proxy/eyJfcmFpbHMiOnsiZGF0YSI6MTgxNjkxNSwicHVyIjoiYmxvYl9pZCJ9fQ%3D%3D--1c254e5de3669f85b7e4bf2ad44f215585690b7e/eyJfcmFpbHMiOnsiZGF0YSI6eyJmb3JtYXQiOiJqcGciLCJyZXNpemVfdG9fZml0IjpbNjAwLDYwMF19LCJwdXIiOiJ2YXJpYXRpb24ifX0%3D--121ebfcd4293f99df590ac1a60ec2d53d6f75b42/40000514251?locale=es",
  "Silk":"https://images.apollo247.in/pub/media/catalog/product/d/a/dai0045_1.jpg",
  "Milkybar":"https://www.londonfoodhall.co.uk/cdn/shop/files/GSS126140_4a229457-8aa2-416f-a7e3-bdc7e33b1367.jpg?v=1715241464",
  "Galaxy":"https://www.galaxychocolate.co.uk/cdn-cgi/image/width%3D600%2Cheight%3D600%2Cf%3Dauto%2Cquality%3D90/sites/g/files/fnmzdf211/files/migrate-product-files/15a129727d8dd6a86c9bff379a99709c5ad68558.png",
  "Amul Chocolate":"https://m.media-amazon.com/images/I/71xJ1o8jGgL._SL1500_.jpg",
  "Free Fire":"https://e.rpp-noticias.io/xlarge/2020/05/23/085408_946319.jpg",
  "PUBG / BGMI":"https://blog.en.uptodown.com/files/2018/07/pubg-featured-hd.jpg",
  "Minecraft":"https://commons.wikimedia.org/wiki/Special:Redirect/file/Minecraft_Beta_1.8.1_Gameplay_Screenshot.png",
  "Valorant":"https://p2.bahamut.com.tw/B/2KU/90/a7f572fe6eba2e30ec4a8adb0a1x2vi5.JPG",
  "Call of Duty":"https://commons.wikimedia.org/wiki/Special:Redirect/file/Call_Of_Duty.jpg",
  "Roblox":"https://cdn.startselect.com/production/blog/preview-images/die-besten-roblox-spiele.jpg?v=1777638756",
  "FIFA":"https://habrastorage.org/getpro/habr/upload_files/dba/b0d/2b8/dbab0d2b80dac3d91093b2e173b4888f.jpg",
  "Cricket 24":"https://commons.wikimedia.org/wiki/Special:Redirect/file/Playing_cricket.jpg",
};

const COLOR_SWATCHES={Black:'#202020',Blue:'#4f91ff',Red:'#ef5574',White:'#eeeeee',Purple:'#8b63df',Green:'#55bd7c','Sky Blue':'#6bcaf1',Pink:'#f28db6',Orange:'#f09b4b',Yellow:'#f2d15b',Peach:'#ffc7a8'};

/* Every non-product option has an explicit, relevant photo-search phrase. */
const PHOTO_ALIASES={
  // Games
  'Free Fire':'free fire mobile game','PUBG / BGMI':'pubg bgmi mobile game','Minecraft':'minecraft game','GTA V':'grand theft auto game','Valorant':'valorant game','Call of Duty':'call of duty game','Roblox':'roblox game','FIFA':'fifa football game','Cricket 24':'cricket game','Fortnite':'fortnite game',
  // Hobbies
  'Gaming':'gaming setup','Cricket':'cricket sport','Football':'football sport','Cycling':'cycling bicycle','Drawing':'drawing art hobby','Music':'music headphones','Coding':'coding laptop','Photography':'photography camera','Watching Movies':'movie theater','Reading':'reading book','Dancing':'dance hobby','Singing':'singing hobby','Cooking':'cooking hobby','Shopping':'shopping mall',
  // Free time
  'Play Games':'gaming controller','Watch Videos':'watching videos laptop','Listen to Music':'listening to music headphones','Talk With Friends':'friends talking','Go Outside':'friends outdoors','Code':'programming laptop','Watch Movies':'watching movies','Sleep':'sleeping bedroom','Scroll Social Media':'social media smartphone','Play Sports':'friends playing sports','Dance':'dance hobby','Gaming':'gaming setup',
  // Music
  'Pop':'pop music concert','Rap':'rap music concert','Lo-fi':'lofi music headphones','Rock':'rock music concert','Bollywood':'bollywood dance music','EDM':'edm dj concert','Romantic':'romantic music','Classical':'classical music orchestra','Hip-Hop':'hip hop music concert','Indie':'indie music concert','K-pop':'kpop concert',
  // Food
  'Pizza':'pizza food','Burger':'hamburger food','Biryani':'biryani food','Noodles':'noodles food','Momos':'momos dumplings food','Chicken':'chicken food','Fried Rice':'fried rice food','Pasta':'pasta food','Roll':'kathi roll food','Dosa':'dosa food',
  // Apps
  'Instagram':'instagram social media phone','YouTube':'youtube video app','WhatsApp':'whatsapp messaging phone','Snapchat':'snapchat social media phone','Telegram':'telegram messaging phone','Spotify':'spotify music phone','Discord':'discord gaming chat','Facebook':'facebook social media phone','Chrome':'google chrome browser laptop','Gaming Apps':'mobile gaming phone',
  // Seasons
  'Summer':'summer sunny beach','Winter':'winter snow cozy','Monsoon':'monsoon rain umbrella','Spring':'spring flowers','Autumn':'autumn leaves',
  // Weekend
  'Trip With Friends':'friends travel trip','Movie Night':'friends movie night','Sleeping':'sleeping bed','Sports':'sports friends','Food Outing':'restaurant friends','Cycling':'cycling friends','Shopping':'shopping mall friends','Staying Home':'cozy home weekend','Music':'music weekend',
  // Movies
  'Action':'action movie cinema','Comedy':'comedy movie cinema','Romance':'romantic movie cinema','Horror':'horror movie cinema','Thriller':'thriller movie cinema','Sci-Fi':'science fiction movie cinema','Animation':'animated movie cinema','Adventure':'adventure movie cinema','Drama':'drama movie cinema','Fantasy':'fantasy movie cinema',
  // Extra visual options
  'Pinterest':'pinterest inspiration app','Cake':'birthday cake dessert','Ice Cream':'ice cream dessert','Hot Chocolate':'hot chocolate mug','Smoothie':'fruit smoothie drink','Spa Day':'spa relaxing self care',
  // Drinks
  'Cold Coffee':'iced coffee','Tea':'tea cup','Coca-Cola':'cola bottle','Sprite':'lemon lime soda','Lemonade':'lemonade drink','Milkshake':'milkshake drink','Mango Shake':'mango smoothie','Juice':'fruit juice','Energy Drink':'energy drink can','Water':'glass of water'
};

function photoQuery(option){
  return (PHOTO_ALIASES[option] || option).toLowerCase().replace(/\//g,' ');
}

/*
 * IMPORTANT:
 * Do not use random-photo services here. They can return an unrelated image
 * (for example a travel photo for a cricket option). The fallback below uses
 * Bing's image-search thumbnail endpoint, so the search term itself controls
 * what visual is returned.
 */
function bingPhoto(option, host='tse1.mm.bing.net'){
  const query = photoQuery(option) + ' real photo';
  return 'https://' + host + '/th?q=' + encodeURIComponent(query) + '&w=900&h=600&c=7&rs=1&p=0';
}

function photoFor(option){
  if(EXACT_PHOTOS[option]) return EXACT_PHOTOS[option];
  /* Colors also get a searched visual instead of a generic dummy image. */
  if(COLOR_SWATCHES[option]){
    const colorQueries={
      Black:'black color aesthetic object photo', Blue:'blue color aesthetic object photo',
      Red:'red color aesthetic object photo', White:'white color aesthetic object photo',
      Purple:'purple color aesthetic object photo', Green:'green color aesthetic object photo',
      'Sky Blue':'sky blue color aesthetic object photo', Pink:'pink color aesthetic object photo',
      Orange:'orange color aesthetic object photo', Yellow:'yellow color aesthetic object photo',
      Peach:'peach color aesthetic object photo'
    };
    PHOTO_ALIASES[option]=colorQueries[option] || option+' color photo';
  }
  return bingPhoto(option);
}

/*
 * If an exact product URL blocks hotlinking, search Bing for that exact item.
 * If the first Bing thumbnail host fails, try another Microsoft thumbnail host.
 * There is deliberately NO Picsum/random-photo fallback.
 */
function imageFallback(img,option){
  const stage=Number(img.dataset.photoFallback || '0');
  if(stage===0){
    img.dataset.photoFallback='1';
    img.src=bingPhoto(option,'tse1.mm.bing.net');
    return;
  }
  if(stage===1){
    img.dataset.photoFallback='2';
    img.src=bingPhoto(option,'tse2.mm.bing.net');
    return;
  }
  img.dataset.photoFallback='3';
  img.alt=option+' photo unavailable';
  img.style.visibility='hidden';
}
