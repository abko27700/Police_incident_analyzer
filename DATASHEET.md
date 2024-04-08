
# Datasheet

## Motivation:

### For what purpose was the dataset created?
The purpose of the dataset is to augment incident data extracted from public police department websites. The augmentation aims to enhance the dataset's usefulness for downstream processes while considering fairness and bias issues.

### Who created the dataset (e.g., which team, research group) and on behalf of which entity (e.g., company, institution, organization)?
Abhishek Kothari from University of Florida created this dataset as part of his course CIS 6930, Spring 2024 Assignment 2.

### Who funded the creation of the dataset? 
This Dataset was not funded, it was part of a course assignment.

### Any other comments?
None. 

## Composition:

### What do the instances that comprise the dataset represent (e.g., documents, photos, people, countries)?
The dataset represents incidents extracted from public police department websites. Each instance denotes a specific incident, including details like day, time, location, nature of incident, and weather.

### How many instances are there in total (of each type, if appropriate)?
The dataset's total instances are derived from incidents in the CSV feed. Each URL represents reports for a day, possibly containing multiple incidents. The datasheet reflects all incidents across URLs.

### Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a larger set? 
The dataset is a sample of instances extracted from incident reports on public police department websites, rather than encompassing all possible incidents.

### What data does each instance consist of? 
Each instance comprises incident details: day, time, weather, location rank, side of town, incident rank, nature, and EMSSTAT.

### Is there a label or target associated with each instance?
Yes, the label or target associated with each instance is the EMSSTAT, indicating emergency medical service status.

### Is any information missing from individual instances?
Yes, information may be missing from individual instances, such as incomplete incident reports or unavailable data fields.

### Are relationships between individual instances made explicit (e.g., users' movie ratings, social network links)? 
Yes, the EMSSTAT logic represents a relationship between individual instances. It indicates whether subsequent incidents at the same time and location are also EMSSTAT-related, suggesting a temporal and spatial relationship between incidents.

### Are there recommended data splits (e.g., training, development/validation, testing)?
Recommended data splits are not specified in the assignment instructions.

### Are there any errors, sources of noise, or redundancies in the dataset?
Yes, errors may arise from defaulting to the center of town coordinates in cases where location coordinates are not found. Noise may occur due to inconsistencies or missing data in incident reports. Redundancies might arise from duplicate or overlapping incident records.

### Is the dataset self-contained, or does it link to or otherwise rely on external resources (e.g., websites, tweets, other datasets)? 
The dataset relies on external resources in the form of incident reports extracted from public police department websites. There are no guarantees that these websites will remain constant over time, as website content may change or be updated. There may not be official archival versions of the complete dataset, including external resources as they existed at the time of creation.

### Does the dataset contain data that might be considered confidential (e.g., data that is protected by legal privilege or by doctor–patient confidentiality, data that includes the content of individuals’ non-public communications)?
No, the dataset does not contain confidential data. It primarily consists of incident reports extracted from public police department websites, which are typically considered public information.

### Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety? 
Yes, the dataset might cause anxiety due to the presence of health issues or violent crimes.

### Does the dataset relate to people?  
No, it does not. 

## Collection Process: 

### How was the data associated with each instance acquired? 
The data associated with each instance was acquired by extracting incident reports from public police department websites.

### What mechanisms or procedures were used to collect the data (e.g., hardware apparatus or sensor, manual human curation, software program, software API)? 
The data associated with each instance was collected using a software program or script designed to extract incident reports from public police department websites. The data collection process involved using APIs such as Google Maps, OpenMeteo, and Geopy.

### If the dataset is a sample from a larger set, what was the sampling strategy (e.g., deterministic, probabilistic with specific sampling probabilities)?
The sampling strategy for creating the dataset is random, where any incident URL could be passed to create the dataset.

### Who was involved in the data collection process (e.g., students, crowdworkers, contractors) and how were they compensated (e.g., how much were crowdworkers paid)?
The data collection process was conducted solely by "Abhishek Kothari," a student. No external individuals or crowdworkers were involved, and there was no compensation provided for the data collection process.

### Over what timeframe was the data collected? 
The timeframe for data collection would depend on the dates of the incident reports contained within the input CSV file. Without specific details from the CSV file, the timeframe cannot be determined.

### Were any ethical review processes conducted (e.g., by an institutional review board)?
No, there were no ethical review processes conducted, such as by an institutional review board.

### Does the dataset relate to people?
No, it does not relate to people. 

## Preprocessing/cleaning/labeling

### Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing, tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)? 
Yes, preprocessing and cleaning of the data were conducted. This included:
- Handling missing location coordinates by defaulting to the center of town coordinates.
- Augmenting the data with additional attributes such as day of the week, time of day, weather, location rank, side of town, incident rank, nature, and EMSSTAT.
- Formatting the data into tab-separated rows.
- Addressing potential errors, noise, and redundancies in the dataset.

### Was the “raw” data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)?
No, the "raw" data was not saved in addition to the preprocessed/cleaned/labeled data.

### Is the software used to preprocess/clean/label the instances available?
The software used to preprocess/clean/label the instances is available on a private GitHub repository and is not accessible to the public at this time.

### Any other comments?
None.

## Uses

### Has the dataset been used for any tasks already? 
No, the dataset has not been used for any tasks yet.

### Is there a repository that links to any or all papers or systems that use the dataset?
No, there is no repository linking to any papers or systems that use the dataset at this time.

### What (other) tasks could the dataset be used for?
The dataset could be used for various tasks, including:
- Predictive modeling: Building machine learning models to predict incident types, locations, or occurrence probabilities.
- Temporal analysis: Analyzing trends and patterns in incident occurrence over time.
- Spatial analysis: Studying geographical distributions and hotspots of incidents.
- Anomaly detection: Identifying unusual or unexpected

 incidents based on historical data.
- Risk assessment: Assessing the likelihood and severity of different types of incidents in specific locations.
- Policy evaluation: Assessing the effectiveness of policies or interventions on incident prevention or response.
- Community engagement: Using incident data to engage with communities and address safety concerns.
- Resource allocation: Optimizing resource allocation for emergency services based on incident trends and locations.
- Decision support: Providing decision-makers with insights derived from incident data to inform planning and response strategies.
- Research: Supporting academic research on topics related to law enforcement, public safety, and emergency management.

### Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses?
The pre-processing step involving defaulting to the center of town coordinates for missing location data may introduce potential biases or inaccuracies into the dataset.

### Are there tasks for which the dataset should not be used?
The dataset should not be used for:
- Making individual-level predictions.
- Ethically sensitive analyses.
- Legal or regulatory decision-making.

### Any other comments?
None.

## Distribution

### Will the dataset be distributed to third parties outside of the entity (e.g., company, institution, organization) on behalf of which the dataset was created? 
- How will the dataset will be distributed (e.g., tarball on website, API, GitHub)?
- When will the dataset be distributed?
- Will the dataset be distributed under a copyright or other intellectual property (IP) license, and/or under applicable terms of use (ToU)? 
- Have any third parties imposed IP-based or other restrictions on the data associated with the instances?
- Do any export controls or other regulatory restrictions apply to the dataset or to individual instances?
- Any other comments?
None.

## Maintenance

### Who will be supporting/hosting/maintaining the dataset?
The dataset will be supported, hosted, and maintained by "Abhishek."

### How can the owner/curator/manager of the dataset be contacted (e.g., email address)?
b.kothari@ufl.edu

### Is there an erratum?
No, there is no erratum reported for the dataset.

### Will the dataset be updated (e.g., to correct labeling errors, add new instances, delete instances)?
Yes, the dataset will be updated with each execution to correct labeling errors, add new instances, or delete instances as needed.

### If the dataset relates to people, are there applicable limits on the retention of the data associated with the instances (e.g., were individuals in question told that their data would be retained for a fixed period of time and then deleted)? 
Since the dataset does not relate to people, there are no applicable limits on the retention of data associated with the instances.

### Will older versions of the dataset continue to be supported/hosted/maintained?
No, older versions of the dataset will not be supported, hosted, or maintained; they will be deleted.

### If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?
Yes, others can extend, augment, build on, or contribute to the dataset as they wish. It is available in CSV format for easy access and manipulation.

### Any other comments?
None.
