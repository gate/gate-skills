// Run from the approved gate-cli checkout: go run -p 1 /path/to/export_cex_cli.go.
// This inspects Cobra registrations only; it never executes a command handler.
package main

import (
	"encoding/json"
	"os"
	"reflect"
	"runtime"

	"github.com/gate/gate-cli/cmd"
	"github.com/spf13/cobra"
	"github.com/spf13/pflag"
)

type flag struct {
	Name     string `json:"name"`
	Type     string `json:"type"`
	Default  string `json:"default"`
	Usage    string `json:"usage"`
	Required bool   `json:"required"`
}

type command struct {
	Path    string `json:"path"`
	Use     string `json:"use"`
	Short   string `json:"short"`
	Long    string `json:"long"`
	Handler string `json:"handler"`
	Source  string `json:"source"`
	Line    int    `json:"line"`
	Flags   []flag `json:"flags"`
}

func main() {
	root := cmd.Root()
	var result []command
	var visit func(*cobra.Command)
	visit = func(c *cobra.Command) {
		// Runnable group nodes only display help; include executable leaves only.
		if c.Runnable() && !c.HasSubCommands() {
			x := command{Path: c.CommandPath(), Use: c.Use, Short: c.Short, Long: c.Long, Flags: []flag{}}
			handler := reflect.ValueOf(c.RunE)
			if c.RunE == nil {
				handler = reflect.ValueOf(c.Run)
			}
			if !handler.IsNil() {
				fn := runtime.FuncForPC(handler.Pointer())
				x.Handler = fn.Name()
				x.Source, x.Line = fn.FileLine(handler.Pointer())
			}
			c.LocalFlags().VisitAll(func(f *pflag.Flag) {
				x.Flags = append(x.Flags, flag{f.Name, f.Value.Type(), f.DefValue, f.Usage, len(f.Annotations[cobra.BashCompOneRequiredFlag]) > 0})
			})
			result = append(result, x)
		}
		for _, child := range c.Commands() {
			visit(child)
		}
	}
	visit(root)
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(result); err != nil {
		panic(err)
	}
}
