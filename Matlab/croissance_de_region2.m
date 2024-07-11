function [segm] = croissance_de_region2(image, marge_erreur,x,y)

if isstring(image)
    I = imread(image);
else
    I=image;
end

if size(I,3)==3
    I = rgb2gray(I);
end

% Lire l'image RGB à partir du fichier et la convertir en tons de gris
taille = size(I);

% Convertir les coordonnées de double en uint16
x = uint16(x);
y = uint16(y);


% Initialisation:
% Créer un élement structurant 
mask = strel('disk',2,0);
% Créer une image binaire représentant la segmentation 
segm = false(taille);
% Au départ, seul le pixel choisi par l'utilisateur fait partie de l'objet)
% Attention: ginput retourne des coordonnées (x,y) mais l'image doit être 
% indexée en termes de (rangée, colonne).
segm(y,x) = true;

% Initialiser segm_precedente pour la condition d'arrêt
% Pour chaque itération l'image binaire segm est mise à jour 
% et l'image segm_precedente contient l'ancienne segmentation.
% Si, à la prochaine itération, segm est identique à segm_precedente, 
% alors l'algorithme a convergé on sort de la boucle, 
% sinon on sauvegarde segm dans segm_precedente et on recommence une nouvelle itération
segm_precedente = false(taille);

% Variable d'affichage
dispMat=zeros(taille);

% Initialisation des variables de travail
segm_contour = [];
inf_mask = zeros(taille);
sup_mask = zeros(taille);

% On compare segm et segm_precedente
% S'ils sont différent alors on continue le traitement
% Sinon on sort de la boucle
while ~isequal(segm_precedente, segm) 

    % Sauvegarder l'ancienne segmentation
    segm_precedente = segm;
        
    % Mettre à jour les statistiques sur la segmentation actuelle:
    % ------------------------------------------------------------
    % 1 - Extraire les intensités des pixels considérés comme faisant 
    % partie de l'objet dans segm
    intensite_objet = double(I(segm == true));
            
    % 2 - Calculer la moyenne et l'écart type des intensité des pixels 
    % faisant actuellement partie de l'objet
    % À COMPLÉTER
    moyenne = mean(intensite_objet);
    ecart_type = std(intensite_objet);
    
           
    % 3 - Mettre à jour la segmentation
    % ------------------
    % 3.1 - Calculer le contour de segm (les pixels non éxplorés directement 
    % adjacents à segm)
    % 3.1.1 - Calculer la dilatation de segm
    segm_dilate = imdilate(segm,mask);
    
    
    % 3.1.2 - Soustraire segm de segm_dilate pour calculer le contour 
    % extérieur de segm
    segm_contour = segm_dilate - segm;
    
    % 3.1.3 - Extraire les coordonnées du contour de segm 
    indices = find(segm_contour);
          
    % 4 - Marquer chaque pixel du contour comme appartenant à l'objet si
    %     son intensité est à moins d'un écart type (+ une marge d'erreur) 
    % de la moyenne des segm
    %     autrement dit, le pixel i est mis à vrai si 
    %        (moyenne - ecart_type) - marge_erreur < I(i) < (moyenne +
    %        ecart_type) + marge_erreur
    
    
    % 4.1 - Calculer l'inégalité inférieure I(i) < (moyenne + ecart_type) + marge_erreur   
    % À COMPLÉTER 
    inf_mask = I(indices) < (moyenne + ecart_type) + marge_erreur;
    
    
    % 4.2 - Calculer l'inégalité supérieure (moyenne - ecart_type) - marge_erreur < I(i)   
    % À COMPLÉTER
    sup_mask = (moyenne - ecart_type) - marge_erreur < I(indices);
            
    
    % 4.3 - Parmi les pixels du contour, extraire les coordonnées des pixels
    % depuis 'indices' qui satisfont simultanément les deux inégalités et 
    % les ajouter à segm
    a_ajouter = indices(inf_mask & sup_mask);
    segm(a_ajouter) = true;
           
    
end


