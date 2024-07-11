function result = savetolatex(table,path,caption,label)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
clear input;
input.data = table;
% input.data.tableColLabels =colname;
% input.data.tableRowLabels  =rowname;
input.tablePlacement = 'H';
% input.dataFormat = {'%.4f'};
input.tableColumnAlignment = 'c';
input.tableBorders = 1;
input.tableCaption = caption;
input.tableLabel = label;
latex = latexTable(input);

% save LaTex code as file
fid=fopen(path,'w');
[nrows,~] = size(latex);
for row = 1:nrows
    fprintf(fid,'%s\n',latex{row,:});
end
fclose(fid);
result=true;
end