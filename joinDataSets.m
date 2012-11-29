
%parse and join NYC datasets '311 Service Requests since 2010' 
%and 'Demographics Stats by Zip Code' on zipcode saving combined, cleansed
%dataset to csv file trainingData.csv
%
clear all;

demogrByZip=load('demogrByZip.mat');
fid = fopen('311_Service_Requests_from_2010_to_Present.csv','r','n','UTF-8');
%store 311 service requests from 2010 to present in cell array skipping
%last cell , Location, which has bad unusable values
serviceRequests=textscan(fid,'%d%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%*[^\n]','delimiter',',');

%only keep cells from 311 data with meaningful attributes
svcRequestsFinal = cell(1,12);
p=1;
for i = [4 5 6 7 8 9 16 17 19 29 30 39]
    svcRequestsFinal{p}=serviceRequests{i};
    p=p+1;
end
svcReqColSize=size(svcRequestsFinal{2},1);
%%


%convert numeric cells to ordinal cells

%remove redundant variables (ie latitude/longitude coordinates since we already have zip)

%join on incident zip with demographic data set
%%
I=cell(size(demogrByZip.untitled,1),13) %cell array to store quartile classifications  for each attribute of interest from demographic data
I(:)={''};
p=1;
%label attribute columns of interest
I{1,1}='pctFemale'
I{1,2}='pctMale'
I{1,3}='pctPacIslander'
I{1,4}='pctLatino'
I{1,5}='pctAmericanIndian'
I{1,6}='pctAsian'
I{1,7}='pctWhite'
I{1,8}='pctBlack'
I{1,9}='pctOther'
I{1,10}='pctEthnicTotal'
I{1,11}='pctPermResidentAlien'
I{1,12}='pctUSCitizen'
I{1,13}='pctRecPublicAssistance'

for i=[4 6 12 14 16 18 20 22 24 28 30 32 40]
    %find third quartiles for a given attribute
    Ind=find(demogrByZip.untitled(:,i)>.75); %find third quartile
    for j=Ind'
        I{j,p}=strcat('Q3_',I{1,p});
    end
    %find second quartiles for a given attribute
    Ind=find(demogrByZip.untitled(:,i)>.25 & demogrByZip.untitled(:,i)<.75); %find third quartile
    for j=Ind'
        I{j,p}=strcat('Q2_',I{1,p});
    end
    %find first quartiles for a given attribute
    Ind=find(demogrByZip.untitled(:,i)>0 & demogrByZip.untitled(:,i)<.25); %find third quartile
    for j=Ind'
        I{j,p}=strcat('Q1_',I{1,p});
    end
    
    p=p+1;
end

%%
%join svcRequestsFinal and I on zip
for j=1:size(I,2) %for each new attribute from demographics data
    NewAttr = cell(svcReqColSize,1);
    %find indx of zip in demographic data
    for i=2:svcReqColSize
        Indx=find(demogrByZip.untitled(:,1)==str2double(svcRequestsFinal{6}{i}));
        if ~isempty(Indx)
            NewAttr{i}=I{Indx,j};
        else
            NewAttr{i}='';
        end
    end
    NewAttr{1}=I{1,j}; %add attr name
    svcRequestsFinal{end+1}=NewAttr;
    
end
%convert cells to csv file using cell2csv

%need a 10893 by 25 cell array to pass into cell2csv
final=cell(svcReqColSize,size(svcRequestsFinal,2));
%%
for i = 1:size(final,2) %cols
    for j = 1:size(final,1) %rows
        final{j,i}= svcRequestsFinal{i}{j};
    end
end
%%
%remove attributes with too many N/A's or too little relevance
%remove agency (redundant), address type, facility type, school name
final(:,[1 7 9 10])=[]

%save to csv
cell2csv('trainingData.csv',final,',');
