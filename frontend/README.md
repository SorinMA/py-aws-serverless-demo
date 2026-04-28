# Frontend Deployment

This frontend is deployed as a static site using AWS S3 and CloudFront.

## Deploy

1. Deploy the infrastructure  
   `serverless deploy --stage dev`

2. Build the frontend  
   `npm run build`

3. Upload the build output to S3  
   `aws s3 sync dist s3://<BucketName> --delete --profile serverlessDev`

4. Invalidate the CloudFront cache  
   `aws cloudfront create-invalidation --distribution-id <DistributionId> --paths "/*" --profile serverlessDev`

## Notes

### Where do I find the `distribution-id`?

You can find it in:
- AWS Console → **CloudFront** → **Distributions** → **The first column is the id**

### How do I check whether the invalidation finished?

`aws cloudfront get-invalidation --distribution-id YOUR_DISTRIBUTION_ID --id YOUR_INVALIDATION_ID --profile serverlessDev`

When the status is `Completed`, the new files should be served.

## Cleanup

1. Empty the S3 bucket  
   `aws s3 rm s3://YOUR_BUCKET_NAME --recursive --profile serverlessDev`

2. Remove the stack  
   `serverless remove --stage dev`