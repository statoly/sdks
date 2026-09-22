# statoly

Official Go client for the [Statoly](https://statoly.ch) API.

```bash
go get github.com/statoly/sdks/go
```

```go
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/statoly/sdks/go"
)

func main() {
	client, err := statoly.New(os.Getenv("STATOLY_TOKEN"))
	if err != nil {
		panic(err)
	}

	monitors, err := client.Monitors().Get(context.Background(), nil)
	if err != nil {
		panic(err)
	}

	for _, monitor := range monitors {
		fmt.Println(*monitor.GetTitle(), *monitor.GetStatus())
	}
}
```

Point it elsewhere with `statoly.New(token, statoly.WithBaseURL("https://…"))`.

Generated from the Statoly OpenAPI document with Microsoft Kiota. Report issues
at [statoly/sdks](https://github.com/statoly/sdks). MIT.
