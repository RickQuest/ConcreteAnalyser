function [segm] = croissance_de_region2(image, marge_erreur,x,y)

if isstring(image)
    I = imread(image);
else
    I=image;
end

if size(I,3)==3
    I = rgb2gray(I);
end

% Lire l'image RGB � partir du fichier et la convertir en tons de gris
taille = size(I);

% Convertir les coordonn�es de double en uint16
x = uint16(x);
y = uint16(y);


% Initialisation:
% Cr�er un �lement structurant 
mask = strel('disk',2,0);
% Cr�er une image binaire repr�sentant la segmentation 
segm = false(taille);
% Au d�part, seul le pixel choisi par l'utilisateur fait partie de l'objet)
% Attention: ginput retourne des coordonn�es (x,y) mais l'image doit �tre 
% index�e en termes de (rang�e, colonne).
segm(y,x) = true;

% Initialiser segm_precedente pour la condition d'arr�t
% Pour chaque it�ration l'image binaire segm est mise � jour 
% et l'image segm_precedente contient l'ancienne segmentation.
% Si, � la prochaine it�ration, segm est identique � segm_precedente, 
% alors l'algorithme a converg� on sort de la boucle, 
% sinon on sauvegarde segm dans segm_precedente et on recommence une nouvelle it�ration
segm_precedente = false(taille);

% Variable d'affichage
dispMat=zeros(taille);

% Initialisation des variables de travail
segm_contour = [];
inf_mask = zeros(taille);
sup_mask = zeros(taille);

% On compare segm et segm_precedente
% S'ils sont diff�rent alors on continue le traitement
% Sinon on sort de la boucle
while ~isequal(segm_precedente, segm) 

    % Sauvegarder l'ancienne segmentation
    segm_precedente = segm;
        
    % Mettre � jour les statistiques sur la segmentation actuelle:
    % ------------------------------------------------------------
    % 1 - Extraire les intensit�s des pixels consid�r�s comme faisant 
    % partie de l'objet dans segm
    intensite_objet = double(I(segm == true));
            
    % 2 - Calculer la moyenne et l'�cart type des intensit� des pixels 
    % faisant actuellement partie de l'objet
    % � COMPL�TER
    moyenne = mean(intensite_objet);
    ecart_type = std(intensite_objet);
    
           
    % 3 - Mettre � jour la segmentation
    % ------------------
    % 3.1 - Calculer le contour de segm (les pixels non �xplor�s directement 
    % adjacents � segm)
    % 3.1.1 - Calculer la dilatation de segm
    segm_dilate = imdilate(segm,mask);
    
    
    % 3.1.2 - Soustraire segm de segm_dilate pour calculer le contour 
    % ext�rieur de segm
    segm_contour = segm_dilate - segm;
    
    % 3.1.3 - Extraire les coordonn�es du contour de segm 
    indices = find(segm_contour);
          
    % 4 - Marquer chaque pixel du contour comme appartenant � l'objet si
    %     son intensit� est � moins d'un �cart type (+ une marge d'erreur) 
    % de la moyenne des segm
    %     autrement dit, le pixel i est mis � vrai si 
    %        (moyenne - ecart_type) - marge_erreur < I(i) < (moyenne +
    %        ecart_type) + marge_erreur
    
    
    % 4.1 - Calculer l'in�galit� inf�rieure I(i) < (moyenne + ecart_type) + marge_erreur   
    % � COMPL�TER 
    inf_mask = I(indices) < (moyenne + ecart_type) + marge_erreur;
    
    
    % 4.2 - Calculer l'in�galit� sup�rieure (moyenne - ecart_type) - marge_erreur < I(i)   
    % � COMPL�TER
    sup_mask = (moyenne - ecart_type) - marge_erreur < I(indices);
            
    
    % 4.3 - Parmi les pixels du contour, extraire les coordonn�es des pixels
    % depuis 'indices' qui satisfont simultan�ment les deux in�galit�s et 
    % les ajouter � segm
    a_ajouter = indices(inf_mask & sup_mask);
    segm(a_ajouter) = true;
           
    
end


