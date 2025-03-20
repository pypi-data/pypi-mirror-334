#
#    Copyright (C) 2021 NDP Systèmes (<http://www.ndp-systemes.fr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# pylint: disable=W0703

import logging
from io import BytesIO
from typing import Dict, Iterable, List, Optional, Tuple, Union

from minio import Minio
from minio.deleteobjects import DeleteObject
from minio.error import S3Error
from odoo_env_config.entry import env_to_section
from odoo_env_config.section import S3Section

_logger = logging.getLogger(__name__)


class S3ConnectInfo:
    def __init__(
        self,
        host: str,
        access_key: str,
        secret: str,
        region: Optional[str] = "us-east-1",
        secure: Optional[bool] = True,
    ):
        self._access_key = access_key
        self._secret = secret
        self._region = region or "us-east-1"
        self._host = host
        self._secure = secure

    @property
    def access_key(self) -> str:
        return self._access_key

    @property
    def secret(self) -> str:
        return self._secret

    @property
    def region(self) -> str:
        return self._region

    @property
    def secure(self) -> bool:
        return self._secure

    @property
    def host(self) -> str:
        return self._host

    @property
    def enable(self) -> bool:
        return bool(self.host and self.secret and self.access_key)

    @property
    def s3_session(self) -> Minio:
        return Minio(
            self.host,
            access_key=self.access_key,
            secret_key=self.secret,
            region=self.region,
            secure=self.secure,
        )


class S3OdooBucketInfo:
    def __init__(self, name: str, sub_dir_name: Optional[str] = None, checklist_dir: Optional[str] = None):
        """
        Represente la configurtation d'un bucket S3
        :param name: LE nom du bucket : obligatoire
        :param sub_dir_name: Non d'un dossie    r inclut lors de la création d'une clef
        :param checklist_dir: Nom du dossier pour faire la gestion des fichiers à supprimer
        """
        assert name
        self.name = name
        self.sub_dir_name = sub_dir_name
        self.checklist_dir = checklist_dir or "checklist"

    def get_key(self, *file_paths: List[str]) -> str:
        """
        Retourne la clef pour la paire db_name et file_name

        Si la connexion (self.conn) à été créée avec **sub_dir_by_db** à Vrai alors le format sera <db_name>/<file_name>
        Sinon uniquement file_names sera retourné séparé par des '/'
        :param file_paths: un tableau de 1 ou n constituant le chemain sous first-dir
        du fichier dans le bucket, supprime les valeur <False>
        :return: self.sub_dir_name/*file_paths ir sub_dir_name is provided
        """
        keys = [f for f in file_paths if f]
        if bool(self.sub_dir_name):
            keys.insert(0, self.sub_dir_name)
        return "/".join(keys)


class S3Odoo:
    def __init__(self, connection: S3ConnectInfo, bucket: S3OdooBucketInfo):
        self.conn = connection
        self.bucket = bucket

    @staticmethod
    def get_connection(
        host: str,
        access_key: str,
        secret: str,
        region: str,
        bucket_name: str,
        secure: Optional[bool] = True,
        db_name: Optional[str] = None,
    ) -> "S3Odoo":
        """
        Créer une instance de S3Odoo avec les parametres fournit.
        `db_name` permet d'avoir un dossier ou tous les enregistrements
         fait par file_write seront automatiquement dedans
         Voir aussi S3ConnectInfo#__init__, S3OdooBucketInfo#__init__
        :param host: le host du serveur S3 fournit par votre fournisseur S3
        :param access_key: la clef d'acces fournit par votre fournisseur S3
        :param secret: le secret d'acces fournit par votre fournisseur S3
        :param region: la region ou se trouve votre S3 fournit par votre fournisseur S3
        :param bucket_name: le nom du bucket à utiliser
        :param secure: Secured connection (https / http)
        :param db_name: le nom du repertoire principal à utiliser dans le bucket
        :return:
        """
        return S3Odoo(
            S3ConnectInfo(
                host=host,
                access_key=access_key,
                secret=secret,
                region=region,
                secure=secure,
            ),
            S3OdooBucketInfo(name=bucket_name, sub_dir_name=db_name),
        )

    @staticmethod
    def from_env(db_name: str = None) -> "S3Odoo":
        s3section = env_to_section(S3Section)
        if s3section.sub_dir and not db_name:
            raise ValueError("db_name not provided but your environ variable to required it are set")
        dbname = db_name if s3section.sub_dir else None
        return S3Odoo.get_connection(
            host=s3section.host,
            access_key=s3section.access_key,
            secret=s3section.secret,
            region=s3section.region,
            bucket_name=s3section.bucket_name,
            secure=s3section.secure,
            db_name=dbname,
        )

    @staticmethod
    def connect_from_env() -> "S3Odoo":
        """
        Créer une connexion au S3 sans prendre en compte le nom de la base de donnée.
        Il faudra donc l'ajouter dans le path de chaque fichier envoyé
        :return: Un connexion au S3 distant depuis les variable d'environement
        """
        s3section = env_to_section(S3Section)
        return S3Odoo.get_connection(
            host=s3section.host,
            access_key=s3section.access_key,
            secret=s3section.secret,
            region=s3section.region,
            bucket_name=s3section.bucket_name,
            secure=s3section.secure,
            db_name=None,
        )

    def get_key(self, *file_paths: List[str]) -> str:
        """
        Voir S3OdooBucketInfo#get_key
        :param file_paths: le path du fichier dans une liste
        :return: le path du fichier
        """
        return self.bucket.get_key(*file_paths)

    def bucket_exist(self) -> bool:
        """
        :return: Vrai si le bucket existe
        """
        return self.conn.s3_session.bucket_exists(self.bucket.name)

    def delete_bucket(self) -> bool:
        """
        Supprime le bucket founit au debut de l'instanciation
        :return: Vrai si la suppression à reussi
        """
        try:
            s3_session = self.conn.s3_session
        except Exception as e:
            _logger.error(
                "S3: delete_bucket Was not able to connect to S3 (%s)",
                e.message,
                exc_info=e,
            )
            return False
        try:
            s3_session.remove_bucket(self.bucket.name)
            return True
        except S3Error as e:
            _logger.error(
                "S3: delete Was not able to delete bucket %s to S3 (%s)",
                self.bucket.name,
                e.message,
                exc_info=e,
            )
        return False

    def create_bucket_if_not_exist(self) -> bool:
        """
        Retourne Vrai **si et uniquement si** le bucket à été créé
        Faut si le bucket existait deja ou si il ya eu une erreur
        :return: Vrai si la création à reussi
        """
        try:
            s3_session = self.conn.s3_session
        except Exception as e:
            _logger.error(
                "S3: create_bucket_if_not_exist Was not able to connect to S3 (%s)",
                exc_info=e,
            )
            return False
        try:
            if not self.bucket_exist():
                s3_session.make_bucket(self.bucket.name)
                _logger.info("S3: bucket [%s] created successfully", self.bucket.name)
                return True
        except S3Error as e:
            _logger.error(
                "S3: create_bucket_if_not_exist Was not able to create bucket %s to S3 (%s)",
                self.bucket.name,
                exc_info=e,
            )
            return False
        return False

    def file_exist(self, fname: str, first_dir: Optional[str] = None) -> bytes:
        """
        Test l'existance du de l'objet avec le nom `fname`
        :param fname: non de l'object dont il faut tester l'existence
        :param first_dir: un dossier parent au fname si besoin
        :return: Vrai si l'object avec le fname existe
        """
        try:
            s3_session = self.conn.s3_session
        except Exception as e:
            _logger.error("S3: _file_read Was not able to connect to S3 (%s)", exc_info=e)
            return b""

        key = self.bucket.get_key(first_dir, fname)
        res = False
        s3_key = None
        try:
            bucket_name = self.bucket.name
            s3_key = s3_session.get_object(bucket_name, key)
            res = True
        except S3Error as e:
            _logger.debug(
                "S3: S3Error _file_read was not able to read from S3 (%s): %s",
                key,
                exc_info=e,
            )
            res = False
        except Exception as e:
            _logger.error("S3: _file_read was not able to read from S3 (%s): %s", key, exc_info=e)
            raise e
        finally:
            if s3_key:
                s3_key.close()
                s3_key.release_conn()
        return res

    def file_read(self, fname: str, first_dir: str = None) -> bytes:
        """
        Lit l'objet avec le nom `fname`
        `first_dir` sert si besoin à preciser un dossier parent
        :param fname: le nom du fichier, peut contenir une arborecence
        :param first_dir: le nom d'un dossier parent
        :return: une valeur binaire
        """
        try:
            s3_session = self.conn.s3_session
        except Exception as e:
            _logger.error("S3: _file_read Was not able to connect to S3 (%s)", e)
            return b""

        s3_key = None
        bucket_name = self.bucket.name
        key = self.bucket.get_key(first_dir, fname)
        try:
            s3_key = s3_session.get_object(bucket_name, key)
            res = s3_key.data
            _logger.debug("S3: _file_read read %s:%s from bucket successfully", bucket_name, key)
        except S3Error as e:
            _logger.debug(
                "S3: S3Error _file_read was not able to read from S3 (%s): %s",
                key,
                exc_info=e,
            )
            return b""
        except Exception as e:
            _logger.error("S3: _file_read was not able to read from S3 (%s): %s", key, exc_info=e)
            raise e
        finally:
            if s3_key:
                s3_key.close()
                s3_key.release_conn()
        return res

    def file_write(self, fname: str, value: bytes, first_dir: str = None) -> str:
        # type: (str, bin, str) -> str
        """
        Ecrit la valeur (`value`) dans le S3 sous le nom `fname`
        `first_dir` permet de préciser un sous dossier si necessaire
        :param fname: nom du fichier, peut contenir l'arboressence complete (Ex: my-dir/file.txt)
        :param value: la valeur binaire
        :param first_dir: un dossier parent au fname
        :return: fname
        """
        try:
            s3_session = self.conn.s3_session
        except S3Error as e:
            _logger.error("S3: _file_write was not able to connect (%s)", e)
            return fname

        bucket_name = self.bucket.name
        key = self.get_key(first_dir, fname)
        try:
            res = s3_session.put_object(bucket_name, key, BytesIO(value), len(value))
            _logger.info(
                "S3: _file_write %s:%s was successfully uploaded => %s",
                bucket_name,
                key,
                res,
            )
        except S3Error as e:
            _logger.error("S3: _file_write was not able to write (%s): %s", key, e)
            raise e
        # Returning the file name
        return fname

    def mark_for_gc(self, fname: str) -> Union[str, None]:
        """
        Met un fichier vide (valeur de 0bytes) dans un sous dossier "checklist" avec le nom fournit en paramettre
        :param fname: le nom du fichier
        :return: fname
        """
        return self.file_write(fname, b"", "checklist")

    def file_delete(self, fname: str) -> bool:
        """
        Supprime le fichier ayant le `fname` et retourne Vrai si il n'y a pas d'erreur
        :param fname: le nom du fichier à supprimer
        :return: Vrai si la suppression ne leve pa d'erreur
        """
        try:
            s3_session = self.conn.s3_session
        except Exception as e:
            _logger.error("S3: file_delete was not able to connect (%s)", e)
            return False
        bucket_name = self.bucket.name
        key = self.bucket.get_key(fname)
        try:
            s3_session.stat_object(bucket_name, key)
            try:
                s3_session.remove_object(bucket_name, key)
                _logger.debug("S3: _file_delete deleted %s:%s successfully", bucket_name, key)
            except Exception as e:
                _logger.error(
                    "S3: _file_delete was not able to gc (%s:%s) : %s",
                    bucket_name,
                    key,
                    e,
                )
                return False
        except Exception as e:
            _logger.error(
                "S3: _file_delete get_stat was not able to gc (%s:%s) : %s",
                bucket_name,
                key,
                e,
            )
            return False
        return True

    def get_checklist_objects(self) -> Dict[str, Tuple[str, str]]:
        checklist = {}
        prefix = self.get_key("checklist")
        # retrieve the file names from the checklist
        for s3_key_gc in self.conn.s3_session.list_objects(self.bucket.name, prefix=prefix, recursive=True):
            if not s3_key_gc.is_dir:
                fname = s3_key_gc.object_name[len(prefix + "/") :]
                real_key_name = fname
                if self.bucket.sub_dir_name:
                    real_key_name = f"{self.bucket.sub_dir_name}/{fname}"
                checklist[fname] = (real_key_name, s3_key_gc.object_name)
        return checklist

    def file_delete_multi(self, to_deletes: Dict[str, str], whitelist: Iterable[str] = None) -> int:
        whitelist = whitelist or []
        removed = 0
        to_mass_deletes = []

        for real_key_name, check_key_name in to_deletes.values():
            to_mass_deletes.append(DeleteObject(check_key_name))
            if not whitelist or real_key_name not in whitelist:
                to_mass_deletes.append(DeleteObject(self.get_key(real_key_name)))

        try:
            errors = list(self.conn.s3_session.remove_objects(self.bucket.name, to_mass_deletes))
            removed = len(to_mass_deletes) and len(to_mass_deletes) - len(errors) or 0
            _logger.debug("S3: _file_gc_s3 deleted %s:%s successfully", self.bucket.name, removed)
        except Exception as e:
            _logger.error("S3: _file_gc_s3 was not able to gc (%s) : %s", self.bucket.name, e)
        return removed
