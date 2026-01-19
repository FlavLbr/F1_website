Structure du projet:


project-root/
│
├── data/
│   ├── raw/        # données API brutes (immutables)
│   ├── staging/    # données nettoyées / normalisées
│   └── mart/       # tables prêtes pour l’analyse / app
│
├── notebooks/
│   ├── 01_exploration/
│   ├── 02_cleaning/
│   └── 03_analysis/
│
├── src/
│   ├── ingestion/
│   ├── transformation/
│   └── utils/
│
├── app/
│   └── dashboard/
│
└── README.md

