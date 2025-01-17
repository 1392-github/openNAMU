package route

import (
	"encoding/json"

	"opennamu/route/tool"
)

func Api_func_ip(call_arg []string) string {
	other_set := map[string]string{}
	json.Unmarshal([]byte(call_arg[0]), &other_set)

	db := tool.DB_connect()
	defer db.Close()

	ip_data := tool.IP_parser(db, other_set["data"], other_set["ip"])

	new_data := make(map[string]interface{})
	new_data["response"] = "ok"
	new_data["data"] = ip_data

	json_data, _ := json.Marshal(new_data)
	return string(json_data)
}
