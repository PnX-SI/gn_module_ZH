type FilesExt = {
  name: string;
  files: ZhFile[];
  editable?: boolean;
};

type ZhFile = {
  id_media: number;
  id_nomenclature_media_type: number;
  id_table_location: number;
  unique_id_media: string;
  uuid_attached_row: string;
  title_fr: string;
  title_en: string | null;
  title_it: string | null;
  title_es: string | null;
  title_de: string | null;
  media_url: string | null;
  media_path: string;
  author: string;
  description_fr: string;
  description_en: string | null;
  description_it: string | null;
  description_es: string | null;
  description_de: string | null;
  is_public: boolean;
  meta_create_date: Date;
  meta_update_date: Date;
  image?: string | ArrayBuffer;
  mainPictureId?: number;
};

type ZhFiles = {
  media_data: ZhFile[];
  main_pict_id: number;
};

export { ZhFile, ZhFiles, FilesExt };
