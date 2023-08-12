class City {
  int postalcode;
  String name;
  float x;
  float y;
  float population;
  float density;
  float altitude;
  float size;
  boolean isHighlighted;
  boolean isDrawn = false ;
  boolean isSelected = false;
  
  void draw( int maxPopulation, int maxAltitude) {
    // calculer la taille du cercle en fonction de la population
    this.size = map(this.population, 0, maxPopulation, 5, 100);
    
    // calculer la couleur en fonction de l'altitude
    color theColor = color(map(this.altitude, 0, maxAltitude, 150, 0), 0, 0);
    
    if (isHighlighted){
      textAlign(LEFT, CENTER);
      textSize(12);
      fill(255, 200);
      rect(mapX(x) + size + 10, mapY(y) - 10, textWidth(name) + 10, 20);
      fill(0);
      text(name, mapX(x) + size + 15, mapY(y));
      fill(0,0,255);
    }
    else if (isSelected){
      textAlign(LEFT, CENTER);
      textSize(12);
      fill(255,200);
      rect(mapX(x) + size + 10, mapY(y) - 10, textWidth(name) + 10, 20);
      fill(255, 100, 00);
      text(name, mapX(x) + size + 15, mapY(y));
      fill(255, 100, 100);
    }
    else {
      fill(theColor);
    }
    ellipse(mapX(this.x), mapY(this.y), size*2, size*2);
    isDrawn = true ;
  }
  
  float mapX(float x) {
  return map(x, minX, maxX, 0, 800);
  }
  
  float mapY(float y) {
  return map(y, minY, maxY, 800, 0);
  }
  
  boolean contains(int px, int py) {
    // Comme nous dessinons un cercle, on utilise ici la distance 
    // entre (px, py) et le centre du cercle,
    // et on ajoute un pixel supplémentaire pour faciliter 
    // la sélection à la souris
    return dist(mapX(x), mapY(y), px, py) <= size + 1 && isDrawn;
  }
}
