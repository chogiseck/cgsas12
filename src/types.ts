export interface NotebookLMConfig {
  projectNumber: string;
  location: string;
}

export interface Notebook {
  name: string;
  displayName: string;
  createTime?: string;
  updateTime?: string;
}

export interface NotebookSource {
  name: string;
  displayName?: string;
  driveSource?: {
    resourceId: string;
  };
  uploadedSource?: {
    fileName: string;
  };
  state?: string;
  createTime?: string;
}

export interface ShareRequest {
  accountAndRoles: Array<{
    email: string;
    role: "PROJECT_ROLE_OWNER" | "PROJECT_ROLE_WRITER" | "PROJECT_ROLE_READER";
  }>;
}

export interface BatchCreateSourcesRequest {
  requests: Array<{
    source: {
      driveSource?: {
        resourceId: string;
      };
    };
  }>;
}

export interface BatchDeleteSourcesRequest {
  names: string[];
}

export interface ListRecentlyViewedResponse {
  notebooks: Notebook[];
  nextPageToken?: string;
}
