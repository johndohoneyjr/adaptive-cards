$URI = 'https://microsoft.webhook.office.com/webhookb2/...'

$JSON = @{
  "@type"    = "MessageCard"
  "@context" = "<http://schema.org/extensions>"
  "title"    = 'Demo Legacy Card--Webhook'
  "text"     = 'Purpose of the card.'
  "sections" = @(
    @{
      "activityTitle"    = 'Test Section'
      "activitySubtitle" = 'Section Subtitle'
      "activityText"     = 'text for the activity in the card, this is the main message.'
    }
  )
} | ConvertTo-JSON

$Params = @{
  "URI"         = $URI
  "Method"      = 'POST'
  "Body"        = $JSON
  "ContentType" = 'application/json'
}

Invoke-RestMethod @Params


$URI = 'https://microsoft.webhook.office.com/webhookb2/...'

# type - Must be set to `message`.
# attachments - This is the container for the adaptive card itself.
# contentType - Must be of the type `application/vnd.microsoft.card.adaptive`.
# content - The header and content of the adaptive card.
# $schema - Must have a value of [`http://adaptivecards.io/schemas/adaptive-card.json`](<http://adaptivecards.io/schemas/adaptive-card.json>) to import the proper schema for validation.
# type - Set to the type of `AdaptiveCard`.
# version - Currently set to version `1.0`.
# body - The content of the card itself to display.

$JSON = [Ordered]@{
  "type"       = "message"
  "attachments" = @(
    @{
      "contentType" = 'application/vnd.microsoft.card.adaptive'
      "content"     = [Ordered]@{
        '$schema' = "<http://adaptivecards.io/schemas/adaptive-card.json>"
        "type"    = "AdaptiveCard"
        "version" = "1.0"
        "body"    = @(
          [Ordered]@{
            "type"  = "Container"
            "items" = @( ## The different contained elements such as TextBlock or an Image.
              @{
                "type"   = "TextBlock"
                "text"   = "Adaptive Test Card"
                "wrap"   = $true ## whether to wrap text that expands past the size of the card itself.
                "weight" = "Bolder" ## Whether to show the card as bolder, lighter, or as the default. If omitted then the text will be shown as default.
                "size"   = "Large" ## The size of the text ranging from small, default, medium, large, or extralarge. If omitted then the text will be shown as default.
              }
              @{
                "type"   = "TextBlock"
                "text"   = "Typically used to describe the purpose of the card."
                "wrap"   = $true
              }
            )
          }
          [Ordered]@{
            "type"  = "Container"
            "style" = "emphasis" ## Two different styles available are emphasis and default.
            "items" = @(
              @{
                "type"   = "TextBlock"
                "text"   = "Test Section"
                "weight" = "Bolder"
                "wrap"   = $true
              }
              @{
                "type"   = "TextBlock"
                "text"   = "Section Subtitle"
                "size"   = "Small"
                "wrap"   = $true
              }
              @{
                "type"   = "TextBlock"
                "text"   = "Descriptive text for the activity."
                "wrap"   = $true
              }
            )
          }
        )
      }
    }
  )
} | ConvertTo-JSON -Depth 20

$Params = @{
  "URI"         = $URI
  "Method"      = 'POST'
  "Body"        = $JSON
  "ContentType" = 'application/json'
}

Invoke-RestMethod @Params
