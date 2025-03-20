import os
import unittest
from unittest.mock import patch

from odoo_filestore_s3.odoo_s3_fs import S3Odoo, S3OdooBucketInfo


class TestWrite(unittest.TestCase):
    def setUp(self):
        """
        Setup d'une connexion sur un bucket généré aléatoirement
        Utilse Cellar de CleverCloud comme fournisseur de S3
        """
        self.conn = S3Odoo.from_env("db_test_write")
        self.assertEqual(self.conn.bucket_exist(), not self.conn.create_bucket_if_not_exist())
        self.assertTrue(self.conn.bucket_exist())

    def tearDown(self):
        """
        Supression des objets S3 et du bucket utilisé pour le test
        """
        for obj in self.conn.conn.s3_session.list_objects(self.conn.bucket.name, recursive=True):
            self.conn.conn.s3_session.remove_object(self.conn.bucket.name, obj.object_name)
        res = list(self.conn.conn.s3_session.list_objects(self.conn.bucket.name))
        self.assertFalse(res)
        self.conn.delete_bucket()
        self.assertFalse(self.conn.bucket_exist())

    def test_file_write(self):
        """
        Test la création d'un objet sur S3 avec une valeur binaire
        """
        fname = "filename.txt"
        self.assertEqual(self.conn.file_write(fname, value=b"My binary content"), fname)
        # Passage par s3_session pour utiliser directement Minio pour tester la création
        res = list(self.conn.conn.s3_session.list_objects(self.conn.bucket.name))
        self.assertTrue(len(res), 1)
        self.assertFalse(res[0].is_dir)
        self.assertEqual(res[0].object_name, fname)

    def test_file_write_sub_folder(self):
        """
        Test la création d'un objet sur S3 avec une valeur binaire
        Le fichier créé ce trouve dans un sous dossier
        """
        dir = "45"
        fname = "filename.txt"
        full_fname = "45/filename.txt"
        self.assertEqual(self.conn.get_key(dir, fname), full_fname)
        self.assertEqual(self.conn.file_write(full_fname, value=b"My binary content"), full_fname)
        # Passage par s3_session pour utiliser directement Minio pour tester la création
        # Récupération du dossier et test que le nom est bien egale à <dir>
        res = list(self.conn.conn.s3_session.list_objects(self.conn.bucket.name))
        self.assertTrue(len(res), 1)
        self.assertTrue(res[0].is_dir)
        self.assertEqual(res[0].object_name, dir + "/")  # S3 ajoute un "/" car c'est un dossier

        # Récupération du fichier avec le path complet
        res = list(self.conn.conn.s3_session.list_objects(self.conn.bucket.name, recursive=True))
        self.assertTrue(len(res), 1)
        self.assertFalse(res[0].is_dir)
        self.assertEqual(res[0].object_name, full_fname)

    def test_file_read_dummy(self):
        """
        Test qu'il n'y ai pas d'erreur lors de la lecture d'un élément qui n'existe pas
        A la place nous attendons un binary vide
        """
        content = self.conn.file_read("file-not-exist")
        self.assertFalse(content)
        self.assertEqual(content, b"")

    def test_file_read(self):
        """
        Test de le création d'un objet S3 et de la lecture
        La lecture doit retourner le contenu envoyer lors de l'écriture
        """
        fname = "filename.txt"
        value = b"My binary content"
        self.assertEqual(self.conn.file_write(fname, value=value), fname)
        retrieve_value = self.conn.file_read(fname)
        self.assertEqual(retrieve_value, value)

    def test_mark_for_gc(self):
        """
        Test que la fonction `mark_for_gc` créé un fichier dans un sous dossier du bucket
        Ce sous dossier a comme valeur "checklist"
        Aucun fichier dans le bucket en dehors du dossier "checklist" ne doit être créé
        Le fichier créé doit être vide car uniquement la presence suffit
        """
        fname = "filename.txt"
        self.conn.mark_for_gc(fname)
        res = list(self.conn.conn.s3_session.list_objects(self.conn.bucket.name, recursive=True))
        self.assertTrue(len(res), 1)
        self.assertFalse(res[0].is_dir)
        self.assertEqual(res[0].object_name, self.conn.get_key("checklist", fname))
        obj = self.conn.conn.s3_session.get_object(self.conn.bucket.name, self.conn.get_key("checklist", fname))
        # Size should be 0 byte
        self.assertEqual(len(obj.data), 0)

    def test_get_checklist_objects(self):
        """
        Test que la focntion `get_checklist_objects` retourne la liste complete des fichier se trouvant dans le
        repertoire "checklist" et uniqueemnt ceci
        """
        self.assertFalse(self.conn.get_checklist_objects())
        self.conn.mark_for_gc("filename.txt")
        checklist_objs = self.conn.get_checklist_objects()
        self.assertEqual(len(checklist_objs), 1)
        self.assertEqual(
            checklist_objs["filename.txt"],
            ("filename.txt", self.conn.get_key("checklist", "filename.txt")),
        )
        self.conn.mark_for_gc("filename2.txt")
        self.assertEqual(len(self.conn.get_checklist_objects()), 2)
        self.assertEqual(
            self.conn.file_write("filename3.txt", value=b"My binary content"),
            "filename3.txt",
        )
        self.assertEqual(len(self.conn.get_checklist_objects()), 2)
        self.conn.mark_for_gc("filename3.txt")
        self.assertEqual(len(self.conn.get_checklist_objects()), 3)

    def test_file_delete(self):
        """
        Test la suppression d'un objet S3
        """
        fname = "filename.txt"
        value = b"My binary content"
        self.assertEqual(self.conn.file_write(fname, value=value), fname)
        res = list(self.conn.conn.s3_session.list_objects(self.conn.bucket.name, recursive=True))
        self.assertTrue(len(res), 1)
        self.assertFalse(res[0].is_dir)
        self.assertEqual(res[0].object_name, fname)
        # Test Delete here

        self.assertTrue(self.conn.file_delete(fname))
        res = list(self.conn.conn.s3_session.list_objects(self.conn.bucket.name, recursive=True))
        self.assertEqual(len(res), 0)

    def test_complete(self):
        """
        Fait un test complet du cycle de vie d'une piece jointe (ir.attachement) Odoo
        - Creation
         - Le marquer pour la suppression
        - Lecture, l'etape d'avant ne le supprime pas -> voir `mark_for_gc`
        - Récupération des objets à supprimer
        - Suppression des objects marqué
        """
        fname = "filename.txt"
        value = b"My binary content"
        # - Création
        self.assertEqual(self.conn.file_write(fname, value=value), fname)
        # - Le marquer pour la suppression
        self.conn.mark_for_gc(fname)
        # - Lecture
        retrieve_value = self.conn.file_read(fname)
        self.assertEqual(retrieve_value, value)
        # - Récupération des objets à supprimer
        checklist_objs = self.conn.get_checklist_objects()
        self.assertEqual(len(checklist_objs), 1)
        self.assertEqual(checklist_objs[fname], (fname, self.conn.get_key("checklist", fname)))
        # - Suppresion
        self.conn.file_delete(fname)
        self.assertFalse(self.conn.file_exist(fname))
        self.assertTrue(self.conn.file_exist(fname, first_dir="checklist"))
        self.conn.file_delete(self.conn.get_key("checklist", fname))
        self.assertFalse(self.conn.file_exist(fname, first_dir="checklist"))

    def test_no_bucket(self):
        new_env = dict(os.environ)
        new_env.pop("ODOO_S3_BUCKET", None)
        with patch.dict(os.environ, new_env, clear=True):
            with self.assertRaises(AssertionError):
                self.conn = S3Odoo.from_env("test_from_env")


class TestRead(unittest.TestCase):
    def test_create_and_delete_bucket(self):
        """
        Test de la création d'un bucket puis de la suppression
        """
        conn = S3Odoo.from_env("db_test_read")
        self.assertEqual(conn.bucket_exist(), not conn.create_bucket_if_not_exist())
        self.assertTrue(conn.bucket_exist())
        conn.delete_bucket()
        self.assertFalse(conn.bucket_exist())

    def test_get_key_bucket(self):
        """
        Test de la création d'un clef pour les fichiers aparture d'un *arg
        Vérification que si un sous dossier obligatoire est utile alors celui-ci est utilisé
        """
        self.assertEqual(S3OdooBucketInfo("b", "my_db").get_key("my-file"), "my_db/my-file")
        self.assertEqual(S3OdooBucketInfo("b").get_key("my-file"), "my-file")
        self.assertEqual(S3OdooBucketInfo("b").get_key("my-file"), "my-file")
        self.assertEqual(S3OdooBucketInfo("b", "").get_key("my-file"), "my-file")
        self.assertEqual(S3OdooBucketInfo("b", None).get_key("my-file"), "my-file")
        self.assertEqual(
            S3OdooBucketInfo("b", "my_db").get_key("my-dir", "my-file"),
            "my_db/my-dir/my-file",
        )
        self.assertEqual(S3OdooBucketInfo("b").get_key("my-dir", "my-file"), "my-dir/my-file")
        self.assertEqual(S3OdooBucketInfo("b", "").get_key("my-dir", "my-file"), "my-dir/my-file")
        self.assertEqual(S3OdooBucketInfo("b", None).get_key("my-dir", "my-file"), "my-dir/my-file")

        binfo = S3OdooBucketInfo("b", "my_db")
        self.assertEqual(binfo.get_key("my-dir", "my-file"), "my_db/my-dir/my-file")
        self.assertEqual(binfo.get_key("my-dir2", "my-file"), "my_db/my-dir2/my-file")
