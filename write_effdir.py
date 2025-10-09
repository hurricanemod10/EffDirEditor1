function WriteEffDir(filename, effdir)
% WriteEffDir - Save an EffDir structure to binary file
%
%   WriteEffDir(filename, effdir)
%
%   filename : output file name
%   effdir   : structure containing all sections 1–15
%
%   This function writes the full Effect Directory format as used
%   in SimCity 4 (Sections 1–15 + 13.5).

fid = fopen(filename,'w','ieee-le'); % little endian

%% ------------------------
%  Section 1
%% ------------------------
fwrite(fid,effdir.sec(1).n_entries,'uint32'); 
for i=1:effdir.sec(1).n_entries
    fwrite(fid,effdir.sec(1).entry(i).u1,'uint32');
    fwrite(fid,effdir.sec(1).entry(i).u2,'uint32');
end
fwrite(fid,effdir.sec(1).eos,'uint16'); 

%% ------------------------
%  Section 2
%% ------------------------
fwrite(fid,effdir.sec(2).n_entries,'uint32'); 
for i=1:effdir.sec(2).n_entries
    fwrite(fid,effdir.sec(2).entry(i).u1,'uint32');
    fwrite(fid,effdir.sec(2).entry(i).resource_key,'uint32');
    fwrite(fid,effdir.sec(2).entry(i).inverse_flg,'uint8');
    fwrite(fid,effdir.sec(2).entry(i).repeat_flg,'uint8');
    fwrite(fid,effdir.sec(2).entry(i).speed,'float32');

    fwrite(fid,effdir.sec(2).entry(i).rotation_over_time_rep,'uint32');
    fwrite(fid,effdir.sec(2).entry(i).rotation_over_time,'float32');

    fwrite(fid,effdir.sec(2).entry(i).size_over_time_rep,'uint32');
    fwrite(fid,effdir.sec(2).entry(i).size_over_time_pc,'float32');

    fwrite(fid,effdir.sec(2).entry(i).alpha_over_time_rep,'uint32');
    fwrite(fid,effdir.sec(2).entry(i).alpha_over_time_pc,'float32');

    fwrite(fid,effdir.sec(2).entry(i).color_adj_over_time_rep,'uint32');
    for j=1:effdir.sec(2).entry(i).color_adj_over_time_rep
        fwrite(fid,effdir.sec(2).entry(i).red(j),'float32');
        fwrite(fid,effdir.sec(2).entry(i).green(j),'float32');
        fwrite(fid,effdir.sec(2).entry(i).blue(j),'float32');
    end

    fwrite(fid,effdir.sec(2).entry(i).y_axis_stretch_over_time_rep,'uint32');
    fwrite(fid,effdir.sec(2).entry(i).y_axis_stretch_over_time_pc,'float32');

    fwrite(fid,effdir.sec(2).entry(i).initial_intensity_var,'float32');
    fwrite(fid,effdir.sec(2).entry(i).initial_size_var,'float32');

    fwrite(fid,effdir.sec(2).entry(i).u2,'float32');
    fwrite(fid,effdir.sec(2).entry(i).u3,'float32');
    fwrite(fid,effdir.sec(2).entry(i).u4,'float32');
    fwrite(fid,effdir.sec(2).entry(i).u5,'float32');
end
fwrite(fid,effdir.sec(2).eos,'uint16'); 

%% ------------------------
%  Section 3
%% ------------------------
fwrite(fid,effdir.sec(3).n_entries,'uint32'); 
for i=1:effdir.sec(3).n_entries
    fwrite(fid,effdir.sec(3).entry(i).u1,'uint32');
    fwrite(fid,effdir.sec(3).entry(i).resource_key,'uint32');
    fwrite(fid,effdir.sec(3).entry(i).u2,'float32');
    fwrite(fid,effdir.sec(3).entry(i).u3,'float32');
end
fwrite(fid,effdir.sec(3).eos,'uint16'); 

%% ------------------------
%  Section 4
%% ------------------------
fwrite(fid,effdir.sec(4).n_entries,'uint32'); 
for i=1:effdir.sec(4).n_entries
    fwrite(fid,effdir.sec(4).entry(i).u1,'uint32');
    fwrite(fid,effdir.sec(4).entry(i).u2,'uint32');
end
fwrite(fid,effdir.sec(4).eos,'uint16'); 

%% ------------------------
%  Section 5
%% ------------------------
fwrite(fid,effdir.sec(5).n_entries,'uint32'); 
for i=1:effdir.sec(5).n_entries
    fwrite(fid,effdir.sec(5).entry(i).u1,'uint32');
    fwrite(fid,effdir.sec(5).entry(i).u2,'uint32');
end
fwrite(fid,effdir.sec(5).eos,'uint16'); 

%% ------------------------
%  Section 6
%% ------------------------
fwrite(fid,effdir.sec(6).n_entries,'uint32'); 
for i=1:effdir.sec(6).n_entries
    fwrite(fid,effdir.sec(6).entry(i).u1,'uint32');
    fwrite(fid,effdir.sec(6).entry(i).u2,'uint32');
end
fwrite(fid,effdir.sec(6).eos,'uint16'); 

%% ------------------------
%  Section 7
%% ------------------------
fwrite(fid,effdir.sec(7).n_entries,'uint32'); 
for i=1:effdir.sec(7).n_entries
    fwrite(fid,effdir.sec(7).entry(i).u1,'uint32');
    fwrite(fid,effdir.sec(7).entry(i).u2,'uint32');
end
fwrite(fid,effdir.sec(7).eos,'uint16'); 

%% ------------------------
%  Section 8
%% ------------------------
fwrite(fid,effdir.sec(8).n_entries,'uint32'); 
for i=1:effdir.sec(8).n_entries
    fwrite(fid,effdir.sec(8).entry(i).u1,'uint16');
    fwrite(fid,effdir.sec(8).entry(i).u2_rep,'uint32');
    for j=1:effdir.sec(8).entry(i).u2_rep
        fwrite(fid,effdir.sec(8).entry(i).u2.u1(j),'float32');
        fwrite(fid,effdir.sec(8).entry(i).u2.u2(j),'float32');
        fwrite(fid,effdir.sec(8).entry(i).u2.str_rep(j),'uint32');
        fwrite(fid,effdir.sec(8).entry(i).u2.str(j,1:effdir.sec(8).entry(i).u2.str_rep(j)),'char');
    end
    fwrite(fid,effdir.sec(8).entry(i).u3,'uint32');  
end

%% ------------------------
%  Section 9
%% ------------------------
fwrite(fid,effdir.sec(9).n_entries,'uint32'); 
for i=1:effdir.sec(9).n_entries
    fwrite(fid,effdir.sec(9).entry(i).u1,'ubit48');
    fwrite(fid,effdir.sec(9).entry(i).sound_resource_key,'uint32');
    fwrite(fid,effdir.sec(9).entry(i).u2,'float32');
    fwrite(fid,effdir.sec(9).entry(i).u3,'float32');
end

%% ------------------------
%  Section 10
%% ------------------------
fwrite(fid,effdir.sec(10).n_entries,'uint32'); 
for i=1:effdir.sec(10).n_entries
    fwrite(fid,effdir.sec(10).entry(i).u1,'float32');
    fwrite(fid,effdir.sec(10).entry(i).u2,'float32');
    fwrite(fid,effdir.sec(10).entry(i).u3,'float32');
end
fwrite(fid,effdir.sec(10).eos,'uint16'); 

%% ------------------------
%  Section 11
%% ------------------------
fwrite(fid,effdir.sec(11).n_entries,'uint32'); 
for i=1:effdir.sec(11).n_entries
    fwrite(fid,effdir.sec(11).entry(i).u1,'uint32');
    fwrite(fid,effdir.sec(11).entry(i).str_rep,'uint32');
    if effdir.sec(11).entry(i).str_rep > 0
        fwrite(fid,effdir.sec(11).entry(i).str(1:effdir.sec(11).entry(i).str_rep),'char');
    end
    fwrite(fid,effdir.sec(11).entry(i).u2,'uint32');
    fwrite(fid,effdir.sec(11).entry(i).u3,'uint32');
    fwrite(fid,effdir.sec(11).entry(i).u4,'uint32');
    fwrite(fid,effdir.sec(11).entry(i).u5,'float32');
    fwrite(fid,effdir.sec(11).entry(i).u6,'float32');
    fwrite(fid,effdir.sec(11).entry(i).u7,'float32');
    fwrite(fid,effdir.sec(11).entry(i).u8,'float32');
    fwrite(fid,effdir.sec(11).entry(i).u9,'float32');
end
fwrite(fid,effdir.sec(11).eos,'uint16'); 

%% ------------------------
%  Section 12
%% ------------------------
fwrite(fid,effdir.sec(12).n_entries,'uint32'); 
for i=1:effdir.sec(12).n_entries
    fwrite(fid,effdir.sec(12).entry(i).u1,'uint32');
    fwrite(fid,effdir.sec(12).entry(i).u2,'uint32');
    fwrite(fid,effdir.sec(12).entry(i).prim_indx_rep,'uint32');
    for j=1:effdir.sec(12).entry(i).prim_indx_rep
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.str_rep(j),'uint32');
        if effdir.sec(12).entry(i).prim_indx.str_rep(j)>0
            fwrite(fid,effdir.sec(12).entry(i).prim_indx.str(j,1:effdir.sec(12).entry(i).prim_indx.str_rep(j)),'char');
        end
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.indx_flag(j),'uint8');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u1(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u2(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u3a(j),'uint32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u3b(j),'uint32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u4(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u5(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u6(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u7(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u8(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u9(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.xshift(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.zshift(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.yshift(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u10(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u11a(j),'ubit40');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u11b(j),'ubit40');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u12(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u13(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u14(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u15(j),'float32');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u16(j),'uint16');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.u17(j),'uint16');
        fwrite(fid,effdir.sec(12).entry(i).prim_indx.indx_key(j),'uint32');
    end

    fwrite(fid,effdir.sec(12).entry(i).sec_indx_rep,'uint32');
    for k=1:effdir.sec(12).entry(i).sec_indx_rep
        fwrite(fid,effdir.sec(12).entry(i).sec_indx.u1(k),'uint32');
        fwrite(fid,effdir.sec(12).entry(i).sec_indx.str_rep(k),'uint32');
        if effdir.sec(12).entry(i).sec_indx.str_rep(k)>0
            fwrite(fid,effdir.sec(12).entry(i).sec_indx.str(k,1:effdir.sec(12).entry(i).sec_indx.str_rep(k)),'char');
        end
        fwrite(fid,effdir.sec(12).entry(i).sec_indx.u2(k),'uint32');
        fwrite(fid,effdir.sec(12).entry(i).sec_indx.index_key(k),'uint32');
    end

    fwrite(fid,effdir.sec(12).entry(i).u3,'uint32');
    fwrite(fid,effdir.sec(12).entry(i).u4,'uint32');
    fwrite(fid,effdir.sec(12).entry(i).u5,'uint32');
    fwrite(fid,effdir.sec(12).entry(i).u6,'uint32');
end

%% ------------------------
%  Section 13
%% ------------------------
for i=1:effdir.sec(12).n_entries+1
    fwrite(fid,effdir.sec(13).entry(i).str_rep,'uint32');
    fwrite(fid,effdir.sec(13).entry(i).str(1:effdir.sec(13).entry(i).str_rep),'char');
    fwrite(fid,effdir.sec(13).entry(i).index_key,'uint32');
end
fwrite(fid,effdir.sec(13).eos1,'uint8');
fwrite(fid,effdir.sec(13).eos2,'uint8');

%% ------------------------
%  Section 13.5 area
%% ------------------------
fwrite(fid,effdir.sec135.u1,'int8');
fwrite(fid,effdir.sec135.u2,'uint32');
fwrite(fid,effdir.sec135.u3,'float32');
fwrite(fid,effdir.sec135.u4,'float32');
fwrite(fid,effdir.sec135.u5,'float32');
fwrite(fid,effdir.sec135.u6,'float32');
fwrite(fid,effdir.sec135.u7,'float32');
fwrite(fid,effdir.sec135.u8,'float32');
fwrite(fid,effdir.sec135.u9,'float32');
fwrite(fid,effdir.sec135.u10,'float32');
fwrite(fid,effdir.sec135.u11,'float32');

%% ------------------------
%  Section 14
%% ------------------------
fwrite(fid,effdir.sec(14).n_entries,'uint32'); 
for i=1:effdir.sec(14).n_entries
    fwrite(fid,effdir.sec(14).entry(i).str_rep,'uint32');
    if effdir.sec(14).entry(i).str_rep > 0
        fwrite(fid,effdir.sec(14).entry(i).str(1:effdir.sec(14).entry(i).str_rep),'char');
    end
    fwrite(fid,effdir.sec(14).entry(i).group_prop,'uint32');
    fwrite(fid,effdir.sec(14).entry(i).instance_prop,'uint32');
end
fwrite(fid,effdir.sec(14).eos,'uint16'); 

%% ------------------------
%  Section 15
%% ------------------------
fwrite(fid,effdir.sec(15).n_entries,'uint32'); 
for i=1:effdir.sec(15).n_entries
    fwrite(fid,effdir.sec(15).entry(i).class_id,'uint32');
    fwrite(fid,effdir.sec(15).entry(i).str_rep,'uint32');
    if effdir.sec(15).entry(i).str_rep > 0
        fwrite(fid,effdir.sec(15).entry(i).str(1:effdir.sec(15).entry(i).str_rep),'char');
    end
end

%% ------------------------
%  Done
%% ------------------------
fclose(fid);

end
