client<llm> Arcade {
    provider "openai"
    options {
        base_url "https://api.arcade.dev/v1"
        api_key env.ARCADE_API_KEY
        tools ["Search.SearchGoogle", "Google.ListEmails"]
        tool_choice "generate"
    }
}

class Reply {
  type "reply" @description(#"
    once the content is ready.
  "#)
  content string @description(#"
    Use triple quote strings for multi-line strings.
  "#)
}

class OauthRequired {
  type "oauth_required"
  service_name string
  url string
}

function BestRestaurant(query: string) -> Reply | OauthRequired {
    client Arcade
    prompt #"
    Be helpful.

    once you are ready, {{ ctx.output_format }}

    {{ _.role('user')}}
    {{ query}}
    "#
}

test TestName {
  functions [BestRestaurant]
  args {
    query #"
      I'm looking for a good restaurant in San Francisco.
    "#
  }
}

test TestName2 {
  functions [BestRestaurant]
  args {
    query #"
      List my emails.
    "#
  }
}
