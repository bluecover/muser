#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from orm.exc import is_duplicate_entry_exception
from orm.orm_mysql import VideoModel
from util import current_timestamp


def find_video_by_id(db: Session, id_: int) ->VideoModel:
    m = db.query(VideoModel).filter(VideoModel.id == id_).first()
    return m


def find_video_by_oss_path(
        db: Session,
        cloud: str, bucket: str, key: str) -> VideoModel:

    m = db.query(VideoModel).filter(
        VideoModel.cloud == cloud,
        VideoModel.bucket == bucket,
        VideoModel.key == key
    ).first()
    return m


def create_video(
        db: Session,
        cloud: str, bucket: str, key: str,
        etag: str = None, mime_type: str = None, size: int = None,
        duration: int = None, width: int = None, height: int = None,
        persistent_id: str = None) ->VideoModel:

    """ Create `video` record if not existed.
        Igonre `Duplicate Entry` error.
    """
    try:
        video = VideoModel(
            cloud=cloud, bucket=bucket, key=key,
            etag=etag, mime_type=mime_type, size=size,
            duration=duration, width=width, height=height,
            persistent_id=persistent_id,
            status=0,
            create_ts=current_timestamp()
        )
        db.add(video)
        db.commit()
        return video

    except IntegrityError as exc:
        db.rollback()
        if is_duplicate_entry_exception(exc):
            return video
        else:
            raise
