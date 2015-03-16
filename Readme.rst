
adm\_locations
==============

Designed to work with `Proof
Admissions <http://proofgroup.com/AdmissionsTools>`__ for those who are
better at spacial things than just reading from a list.

Steps: - Within Proof adm filter down a set to just the records that you
are interested in. |image0| - Then select to view as list, and export as
other |image1| - Choose Comma-Seperated Text and place in the same
directory as the script |image2| - Move all the fields to the export,
and in the default order |image3| - Then within your terminal run
``./csv_to_json.py filename.csv`` using the filename that you just saved
it as.

.. |image0| image:: img/proof-admissions-prospects--ba-filemaker-.png
    :scale: 50 %
.. |image1| image:: img/proof-admissions-prospects--ba-filemaker-1.png
.. |image2| image:: img/export-records-to-file.png
.. |image3| image:: img/specify-field-order-for-export.png
