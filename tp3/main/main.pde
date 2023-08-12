//globally
//declare the min and max variables that you need in parseInfo
float minX, maxX;
float minY, maxY;
int totalCount; // total number of places
int minPopulation, maxPopulation;
int minSurface, maxSurface;
int minAltitude, maxAltitude;

ArrayList<City> citiesList = new ArrayList<City>();
int minPopulationToDisplay = 10000 ;
int barX = 20;
int barY = 20;
int barWidth = width - 2 * barX;
int barHeight = 10;
color barBackground = color(200);
color barFill = color(50, 150, 200);
float barMin = log(1000); // Seuil de population minimum
float barMax = log(10000000); // Seuil de population maximum
float barValue = log(minPopulationToDisplay); // Valeur courante de la barre

City currentCity = null;
City lastCity = null;
City selectedCity = null ;

int populationSliderX = 20;
int populationSliderY = 20;
int populationSliderWidth = 200;
int populationSliderHeight = 20;
boolean isDraggingPopulationSlider = false;

void setup() {
  size(800, 800);
  readData();
}

void draw() {
  background(255);
  for (City city : citiesList) {
    if(city.population > minPopulationToDisplay){
      city.draw(maxPopulation, maxAltitude);
    }
    else{
      city.isDrawn = false;
    }
  } 
  fill(0);
  text("Afficher les populations supérieures à " + minPopulationToDisplay, 10, 10);
  // drawPopulationHistogram();
  // drawAltitudeHistogram();
  
  stroke(0);
  fill(barBackground);
  rect(barX, barY, barWidth, barHeight);
  fill(barFill);
  float barXValue = map(barValue, barMin, barMax, 0, barWidth);
  rect(barX, barY, barXValue, barHeight);
  
}

void drawPopulationHistogram() {
  float binWidth = 50; // largeur de chaque bin
  float maxCount = 0; // pour normaliser les hauteurs
  // calculer le nombre de villes dans chaque bin
  int[] counts = new int[int(maxPopulation / binWidth) + 1];
  for (City city : citiesList) {
    int binIndex = int(city.population / binWidth);
    counts[binIndex]++;
    maxCount = max(maxCount, counts[binIndex]);
  }
  // dessiner l'histogramme
  stroke(0);
  strokeWeight(1);
  textAlign(LEFT, BOTTOM);
  for (int i = 0; i < counts.length; i++) {
    float x = i * binWidth;
    float y = height - map(counts[i], 0, maxCount, 0, height * 0.8);
    float binHeight = height - y;
    
    fill(200);
    rect(x, y, binWidth, binHeight);
    
    fill(0);
    text(counts[i], x + binWidth/2, y - 5);
  }
}

void drawAltitudeHistogram() {
  float binWidth = 50; // largeur de chaque bin
  float maxCount = 0; // pour normaliser les hauteurs
  // calculer le nombre de villes dans chaque bin
  int[] counts = new int[int(maxAltitude / binWidth) + 1];
  for (City city : citiesList) {
    int binIndex = int(city.altitude / binWidth);
    counts[binIndex]++;
    maxCount = max(maxCount, counts[binIndex]);
  }
  // dessiner l'histogramme
  stroke(0);
  strokeWeight(1);
  textAlign(LEFT, BOTTOM);
  for (int i = 0; i < counts.length; i++) {
    float x = i * binWidth;
    float y = height - map(counts[i], 0, maxCount, 0, height * 0.8);
    float binHeight = height - y;
    
    fill(200);
    rect(x, y, binWidth, binHeight);
    
    fill(0);
    text(counts[i], x + binWidth/2, y - 5);
  }
}

void readData() {
  String[] lines = loadStrings("./villes.tsv");
  parseInfo(lines[0]); // read the header line

  for (int i = 2; i < totalCount; ++i) {
    String[] columns = split(lines[i], TAB);
    City city = new City();
    city.postalcode = int(columns[0]);
    city.name = columns[4];
    city.x = float(columns[1]);
    city.y = float(columns[2]);
    city.population = float(columns[5]);
    city.density = city.population / float(columns[6]);
    city.altitude = float(columns[7]);
    citiesList.add(city);
  }
}

void parseInfo(String line) {
  String infoString = line.substring(2); // remove the #
  String[] infoPieces = split(infoString, ',');
  totalCount = int(infoPieces[0]);
  minX = float(infoPieces[1]);
  maxX = float(infoPieces[2]);
  minY = float(infoPieces[3]);
  maxY = float(infoPieces[4]);
  minPopulation = int(infoPieces[5]);
  maxPopulation = int(infoPieces[6]);
  minSurface = int(infoPieces[7]);
  maxSurface = int(infoPieces[8]);
  minAltitude = int(infoPieces[9]);
  maxAltitude = int(infoPieces[10]);
}

float mapX(float x) {
  return map(x, minX, maxX, 0, 800);
}

float mapY(float y) {
  return map(y, minY, maxY, 800, 0);
}

void keyPressed() {
  if (key == '+') {
    minPopulationToDisplay *= 1.1;  // multiplier le seuil par une constante pour l'augmenter
  } else if (key == '-') {
    minPopulationToDisplay /= 1.1;  // diviser le seuil par une constante pour le diminuer
  }
  redraw();  // redessiner la fenêtre avec la nouvelle valeur de seuil
}

void mouseMoved() {
  currentCity = pick(mouseX, mouseY);
  if (currentCity != null && currentCity != lastCity) {
    // println(currentCity.name);
    currentCity.isHighlighted = true; // Mettre en évidence la ville courante
    if (lastCity != null) {
      lastCity.isHighlighted = false; // Enlever la mise en évidence de la dernière ville désignée
    }
    lastCity = currentCity;
  } else if (currentCity == null && lastCity != null) {
    lastCity.isHighlighted = false; // Enlever la mise en évidence si on ne survole plus de ville
    lastCity = null;
  }
  redraw();
}

public City pick(int px, int py) {
  for (int i = citiesList.size() -1 ; i>=0; i--){
    if (citiesList.get(i).contains(px, py)){
      return citiesList.get(i);
    }
  }
  return null;
}

void mousePressed() {
  City clickedCity = pick(mouseX, mouseY);
  if (clickedCity != null && clickedCity != selectedCity) {
    clickedCity.isSelected = true;
    if (selectedCity != null){
      selectedCity.isSelected = false ;
    }
    selectedCity = clickedCity ;
  }
  else{
    if (selectedCity != null){
      selectedCity.isSelected = false;
    }
    selectedCity = null ;
  }
  
  // Vérifier si l'utilisateur a cliqué sur la barre de progression
  if (mouseY >= barY && mouseY <= barY + barHeight) {
    float newValue = map(mouseX - barX, 0, barWidth, barMin, barMax);
    newValue = max(newValue, barMin);
    newValue = min(newValue, barMax);
    barValue = newValue;
    minPopulationToDisplay = (int) pow(2.5 , barValue);
    filterCities();
  }
  
  if (mouseX >= populationSliderX && mouseX <= populationSliderX + populationSliderWidth &&
      mouseY >= populationSliderY && mouseY <= populationSliderY + populationSliderHeight) {
    isDraggingPopulationSlider = true;
  }
  
  redraw();
}

void filterCities() {
  for (City city : citiesList) {
    if (city.population >= minPopulationToDisplay){
      city.draw(maxPopulation, maxAltitude);
    }
  }
}

void mouseDragged() {
  if (isDraggingPopulationSlider) {
    redraw();
  }
}

void mouseReleased() {
  if (isDraggingPopulationSlider) {
    isDraggingPopulationSlider = false;
    redraw();
  }
}
