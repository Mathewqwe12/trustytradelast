// Base64 encoded SVG images for games
const encodeSvg = (svg: string) => {
  return svg.replace(/#/g, '%23');
};

export const gameImages = {
  dota2: 'https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota2_social.jpg',
  csgo: 'https://cdn.cloudflare.steamstatic.com/apps/csgo/images/csgo_social.jpg',
  wow: 'https://blz-contentstack-images.akamaized.net/v3/assets/blt3452e3b114fab0cd/blt5440cbe6b11972e4/6526a4cb4e4e6248b0021cce/WoW_Classic_SoD_Logo_960x540.png',
  genshin: 'https://webstatic.hoyoverse.com/upload/op-public/2022/08/05/ae83df4a27ca27e7b98d54c962010a0e_3430855268735060274.jpg',
  pubg: 'https://cdn.akamai.steamstatic.com/steam/apps/578080/capsule_616x353.jpg',
  placeholder: 'https://placehold.co/600x400?text=No+Image',
} as const;
