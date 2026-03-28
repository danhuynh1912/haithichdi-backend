module "media_platform" {
  source = "../../../modules/media_platform"

  project_name                           = var.project_name
  environment_name                       = var.environment_name
  bucket_name                            = var.media_bucket_name
  writer_role_names                      = var.writer_role_names
  cloudfront_aliases                     = var.cloudfront_aliases
  acm_certificate_arn                    = var.acm_certificate_arn
  cloudfront_price_class                 = var.cloudfront_price_class
  abort_incomplete_multipart_upload_days = var.abort_incomplete_multipart_upload_days
  noncurrent_version_expiration_days     = var.noncurrent_version_expiration_days
  force_destroy                          = var.force_destroy
  tags                                   = var.tags
}
