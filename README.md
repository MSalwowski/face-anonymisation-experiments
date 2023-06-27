# Goal

The goal of this project is to experimentally evaluate the effectiveness of existing methods for anonymizing facial images. By conducting experiments and creating a database of anonymized faces, we aim to assess the level of privacy protection achieved by different techniques. Additionally, impact of anonymization on biometric performance has been evaluated in order to understand how these techniques affect the accuracy and reliability of facial recognition systems. 

# Experiment specification

Anonymisation techniques:
- blackening
- pixelisation
- blurring
- noising
- [DeepPrivacy2](https://github.com/hukkelas/deep_privacy2)

Face recognition space used:
- ArcFace

Face detection model:
- MTCNN

Data sources:
- [FRGC](https://www.nist.gov/programs-projects/face-recognition-grand-challenge-frgc)