// Base64 encoded SVG images for games
const encodeSvg = (svg: string) => {
  return svg.replace(/#/g, '%23');
};

export const gameImages = {
  placeholder: `data:image/svg+xml;charset=UTF-8,${encodeSvg('<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="200" height="200" fill="#f0f0f0"/><text x="50%" y="50%" text-anchor="middle" fill="#999">No Image</text></svg>')}`,
  dota2: `data:image/svg+xml;charset=UTF-8,${encodeSvg('<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="200" height="200" fill="#1a1a1a"/><text x="50%" y="50%" text-anchor="middle" fill="#ff4d4d" font-size="24">Dota 2</text></svg>')}`,
  csgo: `data:image/svg+xml;charset=UTF-8,${encodeSvg('<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="200" height="200" fill="#2a2a2a"/><text x="50%" y="50%" text-anchor="middle" fill="#ffcc00" font-size="24">CS:GO</text></svg>')}`,
  wow: `data:image/svg+xml;charset=UTF-8,${encodeSvg('<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="200" height="200" fill="#003366"/><text x="50%" y="50%" text-anchor="middle" fill="#ffcc00" font-size="20">World of Warcraft</text></svg>')}`,
  genshin: `data:image/svg+xml;charset=UTF-8,${encodeSvg('<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="200" height="200" fill="#4d1933"/><text x="50%" y="50%" text-anchor="middle" fill="#ff99cc" font-size="20">Genshin Impact</text></svg>')}`,
  pubg: `data:image/svg+xml;charset=UTF-8,${encodeSvg('<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg"><rect width="200" height="200" fill="#333300"/><text x="50%" y="50%" text-anchor="middle" fill="#ffff99" font-size="24">PUBG</text></svg>')}`,
};
