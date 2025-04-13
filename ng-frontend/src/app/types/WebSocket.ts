export type WebSocketBaseMessage = {
  uuid: string;
}

export type WebSocketFetchJsonKey = {
  env: string; // usually name of the file, in the base path
  type: "fetch";
  key: string; // (any key)
}

export type WebSocketUpdateJsonKey = {
  env: string; // usually name of the file, in the base path
  type: "update";
  key: string; // (any key)
  value: string; // (any value)
};

export type WebSocketJsonKeyArgs = WebSocketFetchJsonKey | WebSocketUpdateJsonKey;

export type WebSocketGetFileContentArgs = {
  project: string; // project name, same as folder
  file_name: string; // ^[\w,\s-]+\.[A-Za-z]{3}$
  type: "get_file"; // "get_file"
};

export type WebSocketSetFileContentArgs = {
  project: string; // project name, same as folder
  file_name: string; // ^[\w,\s-]+\.[A-Za-z]{3}$
  type: "set_file"; // "set_file"
  value: string; // (any value) if set_file
};

export type WebSocketFileContentArgs = WebSocketGetFileContentArgs | WebSocketSetFileContentArgs;

export type WebSocketMessage = ({
  type: "json-key";
  args: WebSocketJsonKeyArgs;
} | {
  type: "file-content";
  args: WebSocketFileContentArgs;
}) & WebSocketBaseMessage;

// error response
export type WebSocketErrorResponse = {
  type: "error";
};

export type WebSocketOkResponse = {
  type: "ok";
  uuid: string;
};


export type WebSocketResponse = {
  uuid: string;
} & (WebSocketOkResponse | WebSocketErrorResponse);


