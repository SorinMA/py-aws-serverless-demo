# Frontend Deployment

This frontend is deployed as a static site using AWS S3 and CloudFront.

## Deploy

1. Deploy the infrastructure  (choose one of the following options):
    1. **For Serverless-native and readable**  
   `serverless deploy --stage dev; serverless info --stage dev --verbose`

    2. **For maximum reliability + no Serverless dependency after deploy**  
   `serverless deploy --stage dev; aws cloudformation describe-stacks --stack-name frontend-dev --region eu-north-1 --profile serverlessDev --query "Stacks[0].Outputs"`

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