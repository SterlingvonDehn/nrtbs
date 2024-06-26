'''20240620 initial template to be modified accordingly'''
import os
from misc import extract_date

def generate_slide_frames(title, filenames1, filenames2, comments=''):
    # Initialize an empty string to accumulate LaTeX code
    latex_content = ''

    # Generate LaTeX code for each filename in the list
    for filename in filenames1:
        date = filename.split('/')[-1].split('_')[0]
        for file in filenames2:
            if file.split('/')[-1].split('_')[0]== date:
                slide_number = os.path.splitext(os.path.basename(filename))[0]
                comment_str = comments.replace("#","\\#")
                x = rf'\framesubtitle{{\url{{{comment_str}}}}}' if comments != '' else ''
                latex_content += rf'''
\begin{{frame}}[fragile]{{{title}}}
    \frametitle{{{title}}}
    \begin{{columns}}
        \begin{{column}}{{0.5\textwidth}}
            \centering
            \includegraphics[width=1.1\linewidth,height=1.3\textheight,keepaspectratio]{{{file}}}
        \end{{column}}
        \begin{{column}}{{0.5\textwidth}}
            \centering
            \includegraphics[width=1.1\linewidth,height=1.3\textheight,keepaspectratio]{{{filename}}}
        \end{{column}}
    \end{{columns}}
    {x}
\end{{frame}}
    '''

    return latex_content

# Example usage:
# List of filenames and comments for each slide set
dir_list = ['BARC_timeseries_fort_nelson_cut_composite','MRAP_images','BARC_timeseries_fort_nelson_L2','L2_images','clipped_BARC', 'non_clipped_BARC', 'noise_reduced', 'non_noise_reduced']
slide_list = [[] for i in range(len(dir_list))]

for i in range(len(dir_list)):
    files = os.listdir(dir_list[i])
    file_list = []
    for n in range(len(files)):
        if files[n].split('.')[-1] == 'png':
            file_list.append([files[n].split('_')[0], f'{dir_list[i]}/{files[n]}'])
        else:
            continue;
    file_list.sort()
    
    slide_list[i] = [f[1] for f in file_list]


slide_set1 = slide_list[0]
slide_set2 = slide_list[1]
slide_set3 = slide_list[2]
slide_set4 = slide_list[3]
slide_set5 = slide_list[4]
slide_set6 = slide_list[5]
slide_set7 = slide_list[6]
slide_set8 = slide_list[7]
# LaTeX preamble and end code
latex_preamble = r'''
\documentclass[aspectratio=169]{beamer}
\usepackage{hyperref}
\usepackage{graphicx}
\usepackage{array}
\title{BARC}
\author{Sterling von Dehn and Ash Richardson}
\institute{B.C. Wildfire Service}
\date{\today}

\begin{document}

\begin{frame}
	\titlepage
\end{frame}


\begin{frame}
	\frametitle{Table of Contents}
	\tableofcontents % Automatically generates the table of contents
\end{frame}

\begin{frame}
    \frametitle{Based on Sasha Nasonova's implementation of BARC}
    \framesubtitle{\url{https://github.com/SashaNasonova/burnSeverity}}
    \includegraphics[width=\textwidth]{BARC.png}
\end{frame}
'''

latex_end = r'''
\end{document}
'''

# Make the presentation

with open('presentation.tex', 'w') as file:
    file.write((latex_preamble + r'''\section{Notebook}''' +
                generate_slide_frames('BARC classes/ Google Earth Engine/ Full scene + clipped', slide_set5, slide_set6 ) + r'''\section{Comparisons}''' +
                generate_slide_frames('Local implementation + Google Earth Engine',slide_set6,slide_set8) + r'''\section{Noise reduction}''' + 
                generate_slide_frames('Local implementation + noise reduction',slide_set7,slide_set8,'https://github.com/SterlingvonDehn/nrtbs/blob/9f11f558c7910a31977faae5bdcd278d85b8f25c/dNBR.py#L115') +
                r'''\section{MRAP Data}''' +
                generate_slide_frames('SWIR + BARC/ time series/ MRAP', slide_set1, slide_set2 ) + r'''\section{L2 Data}''' +
                generate_slide_frames('SWIR + BARC/ time series/ L2', slide_set3, slide_set4 )
                + latex_end
                ).replace('_','\\_')) 
    
os.system('pdflatex presentation.tex; rm *.log *.nav *.aux *.snm *.vrb; open presentation.pdf')

