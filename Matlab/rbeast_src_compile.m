function rbeast_src_compile()
% <strong>rbeast_src_compile</strong>: Generate a mex library "Rbeast.mex" 
% tuned for your local machine. If the default mex file (e.g., Rbeast.mexw64 for
% Windows, Rbeast.mexa65 for Linux) is not working. Run this command to download 
% all the C/C++ source files from Github to a local folder named "source" and complie 
% for your own Rbeast.mex. You must have a gcc-like compiler installed and configurred
% appropirately for Matlab. There is a high chance of failure if the compiler setting
%b on your machine is not standard.
%
% If you really need your own version of Rbeast.mex rather than the defualt
% one provided and this script doesn't work. Contact Dr. Kaiguang Zhao at
% zhao.1423@osu.edu for support
%
%%
% codeitself = webread('https://b.link/cmex',weboptions('CertificateFilename',''));
%%
beastPath=rbeast_path() ;
if isempty(beastPath)
	fprintf("Seems like that the Rbeast code is not installed. Please run 'rbeast_install' first to downloadd and install the program from Github.\n" );
	return;
end
%% The list of C headers and source files
f1={  '_beastv2_gui_plot.c'                , ...
    '_beastv2_gui_winmain.c'             , ...
    'abc_common.c'                       , ...
    'abc_cpu.c'                          , ...
    'abc_date.c'                         , ...
    'abc_dir.c'                          , ...
    'abc_ide_util_common.c'                     , ...
    'abc_ide_util_R.c'                     , ...
    'abc_ide_util_matlab.c'                     , ...
    'abc_ide_util_python.c'                     , ...
    'abc_ioFlush.c'                      , ...
    'abc_lzw.c'                          , ...
    'abc_mat.c'                          , ...
    'abc_math.c'                         , ...
    'abc_math_avx.c'                     , ...
    'abc_math_avx512.c'                  , ...
    'abc_mcmc.c'                         , ...
    'abc_mem.c'                          , ...
    'abc_mem_ext.c'                      , ...
    'abc_pthread.c'                      , ...
    'abc_rand_pcg_global.c'              , ...
    'abc_rand_pcg_local.c'               , ...
    'abc_rand_pcg_local_avx2.c'          , ...
    'abc_rand_pcg_local_avx512.c'        , ...
    'abc_rand_pcg_local_generic.c'       , ...
    'abc_sort.c'                         , ...
    'abc_svd.c'                          , ...
    'abc_system.c'                       , ...
    'abc_timer.c'                        , ...
    'abc_ts_func.c'                      , ...
    'abc_tranpose.c'                      , ...
    'abc_vec.c'                          , ...
    'abc_vec_avx2.c'                     , ...
    'abc_vec_avx512.c'                   , ...
    'abc_vec_generic.c'                  , ...
    'abc_win32_demo.c'                   , ...
    'beastv2_COREV4.c'                   , ...
    'beastv2_COREV4_gui.c'               , ...
    'beastv2_COREV4_mthrd.c'             , ...
    'beastv2_basis_allocinitmem.c'       , ...
    'beastv2_basis_computexy_q.c'        , ...
    'beastv2_basis_cvtKnotsToBinVec.c'   , ...
    'beastv2_basis_genrandbasis.c'       , ...
    'beastv2_basis_gensegment.c'         , ...
    'beastv2_basis_pickcmptId.c'         , ...
    'beastv2_basis_proposeNew_q.c'       , ...
    'beastv2_basis_updateKsKe_prec0123.c', ...
    'beastv2_basis_updategoodvec.c'      , ...
    'beastv2_func_q.c'                   , ...
    'beastv2_io_in_args.c'               , ...
    'beastv2_io_in_readts.c'             , ...
    'beastv2_io_out_allocmem_q.c'        , ...
    'beastv2_io_out_printargs.c'         , ...
    'beastv2_io_out_write_q.c'           , ...
    'beastv2_io_out_tsextractprint.c'    , ...
    'beastv2_model_allocinit_q.c'        , ...
    'beastv2_prior_model.c'              , ...
    'beastv2_prior_precfunc.c'           , ...
    'beastv2_xxyy_allocmem_q.c'          , ...
    'beastv2_date.c'                     , ...
    'globalvars.c'                       , ...
    'glue_code.c'                        ,  ...
    'tetris.c'                           ,...
    'beastv2_svdbasis.c' ...
    };
f2={ 'abc_000_macro.h'          , ...
    'abc_000_warning.h'        , ...
    'abc_001_config.h'         , ...
    'abc_blas_lapack_lib.h'    , ...
    'abc_blas_lapack_mkl.h'    , ...
    'abc_blas_lapack_myl.h'    , ...
    'abc_blas_lapack_myl_old.h', ...
    'abc_common.h'             , ...
    'abc_cpu.h'                , ...
    'abc_datatype.h'           , ...
    'abc_date.h'               , ...
    'abc_dir.h'                , ...
    'abc_dirent.h'             , ...
    'abc_ide_util.h'           , ...
    'abc_mat.h'                , ...
    'abc_math.h'               , ...
    'abc_math_avx.h'           , ...
    'abc_math_avx512.h'        , ...
    'abc_mcmc.h'               , ...
    'abc_mem.h'                , ...
    'abc_mem_ext.h'            , ...
    'abc_pthread.h'            , ...
    'abc_rand.h'               , ...
    'abc_rand_mkl.h'           , ...
    'abc_rand_pcg_global.h'    , ...
    'abc_rand_pcg_local.h'     , ...
    'abc_sort.h'               , ...
    'abc_system.h'             , ...
    'abc_tranpose.h'          , ...
    'abc_timer.h'              , ...
    'abc_ts_func.h'            , ...
    'abc_vec.h'                , ...
    'abc_win32_demo.h'         , ...
    'beastv2_func.h'           , ...
    'beastv2_header.h'         , ...
    'beastv2_header_solaris.h' , ...
    'beastv2_io.h'             , ...
    'beastv2_model_allocinit.h', ...
    'beastv2_prior_precfunc.h' , ...
    'beastv2_xxyy_allocmem.h'  , ...
    'globalvars.h'             };

fList=[f1,f2];

srcpath = fullfile(beastPath,'source');
if ~exist(srcpath,"dir")
    mkdir(srcpath);
end

%%
isOctave = exist('OCTAVE_VERSION', 'builtin') ~= 0;
%%
rpath = "https://github.com/zhaokg/Rbeast/raw/master/Source/";
fprintf("<strong>Check if all the C/C++ source files have been downloaded or not;  if not, downloading them </strong>...\n" );
fprintf("<strong> from github.com/zhaokg/Rbeast to your local folder </strong>...\n" );
for i=1:numel(fList)
	fn     = fList{i};                   %fn    = string(datalist{i});
    lfile  = fullfile(srcpath,fn);
	rfile  = strcat(rpath, fn);          %rfile = rpath+"testdata/"+fn;    
	if exist(lfile,"file")
      continue;
    end        
    if isOctave
	  urlwrite(rfile,lfile);
	else
	  websave(lfile, rfile,weboptions('CertificateFilename',[]));
    end    
    fprintf('Downloaded: %s\n', lfile);
end
fprintf("<strong>All the required source files are saved under %s /strong> ...\n",srcpath);

%%

%clang  -mmacosx-version-min=10.13 -dynamiclib  -fPIC -I"/Library/Frameworks/R.framework/Resources/include" -I/usr/local/include 
% -I/Applications/MATLAB_R2019b.app/extern/include/ -DM_RELEASE -Wall -O2  -Wl,-headerpad_max_install_names -undefined dynamic_lookup 
% -single_module -multiply_defined suppress -L/Library/Frameworks/R.framework/Resources/lib -L/usr/local/lib -L/Applications/MATLAB_R2019b.app/bin/maci64/ -lpthread -lm -lut -lmwservices -lmat -lmex -lmx *.c -o Rbeast.mexmaci64

flags = "";
libs  = {'-lm'};
if ismac()
   rbeastFile='Rbeast.mexmaci64';   
   flags =' -dynamiclib -Wl,-headerpad_max_install_names -undefined dynamic_lookup -single_module -multiply_defined suppress';
   %flags ={'-mmacosx-version-min=10.13', '-dynamiclib' , '-Wl,-headerpad_max_install_names', '-undefined', 'dynamic_lookup','-single_module', '-multiply_defined', 'suppress'};
elseif isunix() % true for linux and mac
   rbeastFile='Rbeast.mexa64';
elseif ispc()
   rbeastFile='Rbeast.mexw64';
   libs=[libs, '-lkernel32', '-lgdi32', '-luser32'];
end

%%
srcFiles = fullfile(srcpath,'*.c');    %   a wildcard "*.c" is only acceptable for Matlab's Mex not Octave
mexFile  = fullfile(srcpath,'Rbeast');  % no extension to Rbeast, let the system dtermine the extension by itself

srcFiles={};
for i=1:numel(f1)
   srcFiles = [ srcFiles, fullfile(srcpath, f1{i}) ];
   %srcFiles=[ allFiless,   f1{i}, '   ' ];   % this works only in Matlab's mex
end
%%
% https://stackoverflow.com/questions/76672265/in-octave-how-to-compile-a-mex-file-from-multiple-c-c-source-files/76674121#76674121
% A big thanks to  Cris Luengo at https://www.crisluengo.net/
%
%  mex('a.c b.c') is working in Matlab not in Ocatve
%  mex ('a.c','b.c') is working for both

% srcFiles://stackoverflow.com/questions/50894231/pass-contents-of-cell-array-as-individual-input-arguments-to-a-function-in-matla
% allFiless= {'abc_mem.c','abc_vec.c'}
% mex('a.c','b.c') is the same as  mex(files{:})
% '-lmwservices',  '-lut', ":  not avaialble for ocative :

%%
fprintf("<strong>Compiling the C/C++ source files into a mex ....</strong>\n" );

if isOctave

	% https://stackoverflow.com/questions/45234314/matlab-calling-functions-without-parentheses
	% Command syntax vs Function call
    %
	% mex -v CFLAGS='-DM_RELEASE -UUSE_MEX_CMD -fPIC -O2 -Wall -std=gnu99 -mfpmath=sse -msse2 -mstackrealign' -lmwservices -lut *.c -output Rbeast
    % mwz ('-v', "CFLAGS='-DM_RELEASE -UUSE_MEX_CMD -fPIC -O2 -Wall-std=gnu99 -mfpmath=sse -msse2 -mstackrealign'", ...

	cflags    = "CFLAGS=-pthread -DM_RELEASE -UUSE_MEX_CMD -fPIC -O2 -Wall -std=gnu99 -mfpmath=sse -msse2 -mstackrealign";
    
	try   
		mex('-output', mexFile , '-v',  '-pthread', '-DM_RELEASE', '-DO_INTERFACE','-UUSE_MEX_CMD', '-fPIC', '-O2', '-Wall', '-std=gnu99', '-mfpmath=sse', '-msse2', '-mstackrealign','-lpthread',libs{:},  srcFiles{:} );      
		fprintf("\n\n\n<strong>The mex file '%s' has been generated. Please manually move it to the upper-level dirtectory to replace the pre-compiled mex file.</strong>\n", mexFile );
	catch e
		fprintf("\n\n\nError: %s\n", e.message);
		fprintf("<strong>Failed to compile the C files into mex. You must have a complier appropriately set up in Matlab.</strong>\n" );
	end
else

	% srcFiles = fullfile(srcpath,'*.c');
    % mex ('*.c') works for Matlab but not  in Ocatve
    % for consisitency, files are hardcoded
	cflags   =  "CFLAGS=-pthread -DM_RELEASE -UUSE_MEX_CMD -fPIC -O2 -Wall -std=gnu99 -mfpmath=sse -msse2 -mstackrealign";

	try
		mex('-output', mexFile , '-v', cflags+flags,'-lmwservices',  '-lut', '-lpthread', libs{:},  srcFiles{:} );
		fprintf("\n\n\n<strong>The mex file '%s' has been generated. Please manually move it to the upper-level dirtectory to replace the pre-compiled mex file.</strong>\n", mexFile );
	catch e
		fprintf( "\n\n\nError: %s\n", e.message);
		fprintf("<strong>Failed to compile the C files into mex. You must have a complier appropriately set up in Matlab.</strong>\n" );
	end

end
