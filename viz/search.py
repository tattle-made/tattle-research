import numpy as np
from tqdm import tqdm
from viz.db import mongoDB, sqlDatabase
from viz.analyzer import doc2vec, img2vec


class ImageSearch:
    def __init__(self, db_type, db_filename, threshold=20):
        self.ids = []  # id of images in vec db ~ self.vecs
        self.vecs = []  # holds all features
        self.thresh = threshold  # ?
        self.db_type = db_type
        self.db_filename = db_filename
        self.build()  # builds db of features for all images in db in self.vec

    def build(self):
        """
        builds a set of image features in self.vecs
        from those stored in mongodb
        """
        if self.db_type == "mongo":
            db = mongoDB()
            docs = db.docs

            cur = docs.find({"has_image": True})
            total_docs = docs.count_documents({"has_image": True})
            for doc in tqdm(cur, total=total_docs):
                if doc.get("image_vec") is None:
                    continue
                self.ids.append(doc.get("doc_id"))
                self.vecs.append(doc.get("image_vec"))
        elif self.db_type == "sqlite":
            db = sqlDatabase(self.db_filename)
            # TODO: a nicer way to get count
            total_docs = db.query("SELECT COUNT(doc_id) from documents")[0][0]
            cur = db.query(
                "SELECT doc_id, imagevec from documents where imagevec != 'null'"
            )
            for doc in tqdm(cur, total=total_docs):
                self.ids.append(doc[0])
                self.vecs.append(doc[1])
        elif self.db_type == "testing":
            """setup up local testing dataset

            db_filename {list(tuple)}: [(doc_id, vec),...]
            """
            for i, img in tqdm(self.db_filename):
                try:
                    vec = img2vec(img)
                    # insert template doc into search set
                    self.ids.append(i)
                    self.vecs.append(vec.tolist())
                except Exception as e:
                    print(f"{i}: {e}")

        self.vecs = np.array(self.vecs)

    def update(self, doc_id, vec):  # add image to vec db
        self.ids.append(doc_id)
        self.vecs = np.vstack((self.vecs, vec))
        print("updated")

    def search(self, vec, n=1):
        """
        returns [(ids, dist),...] of self.vecs closest to input vec
        """
        if type(vec) == list:  # why is it ever a list
            vec = np.array(vec)
        # np.broadcasting search over entire database
        dists = np.linalg.norm(self.vecs - vec, axis=1)
        idx = np.argsort(dists)

        ret = []
        for i in range(n):
            if dists[idx[i]] < self.thresh:
                ret.append((self.ids[idx[i]], dists[idx[i]]))
        if len(ret) == 0:
            return [(None, None)]
        else:
            return ret


class DocSearch:
    def __init__(self, db_type="mongo", db_filename=None, threshold=1):
        self.ids = []
        self.vecs = []
        self.thresh = threshold
        self.db_type = db_type
        self.db_filename = db_filename
        self.build()

    def build(self):
        if self.db_type == "mongo":
            db = mongoDB()
            docs = db.docs

            cur = docs.find({"has_text": True})
            total_docs = docs.count_documents({"has_text": True})
            for doc in tqdm(cur, total=total_docs):
                if doc.get("text_vec") is None:
                    continue
                self.ids.append(doc.get("doc_id"))
                self.vecs.append(doc.get("text_vec"))
        elif self.db_type == "sqlite":
            db = sqlDatabase(self.db_filename)
            # TODO: a nicer way to get count
            total_docs = db.query("SELECT COUNT(doc_id) from documents")[0][0]
            cur = db.query("SELECT doc_id, vec from documents where vec != 'null'")
            for doc in tqdm(cur, total=total_docs):
                self.ids.append(doc[0])
                self.vecs.append(doc[1])
        elif self.db_type == "testing":
            """setup up local testing dataset

            db_filename {list(tuple)}: [(doc_id, vec),...]
            """
            for i, doc in self.db_filename:
                vec, lang = doc2vec(doc)
                if lang is None:
                    # bad example doc
                    print(f"{vec}: doc no. {i}")
                    continue

                # insert template doc into search set
                self.ids.append(i)
                self.vecs.append(vec.tolist())

        self.vecs = np.array(self.vecs)

    def update(self, doc_id, vec):
        """update class variable self.vecs with new doc

        Arguments:
            doc_id {int} -- unique id for mongodb
            vec {list} -- embedding from doc2vec
        """
        self.ids.append(doc_id)
        self.vecs = np.vstack((self.vecs, vec))

    def search(self, vec):
        if type(vec) == list:
            vec = np.array(vec)

        if vec is None:
            print("vec is None")
            return (None, None)
        dists = np.linalg.norm(self.vecs - vec, axis=1)
        idx = np.argsort(dists)
        if dists[idx[0]] < self.thresh:
            return (self.ids[idx[0]], dists[idx[0]])
        else:
            return (None, None)


if __name__ == "__main__":
    # search = ImageSearch()
    # print(search.search(np.zeros(512).tolist()))

    # search = DocSearch()
    # print(search.search(np.zeros(300).tolist()))
    pass
