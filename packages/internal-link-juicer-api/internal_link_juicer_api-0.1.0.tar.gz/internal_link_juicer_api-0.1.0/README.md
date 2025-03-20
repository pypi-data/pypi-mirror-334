# internal-link-juicer-api-client
A Python client for the  Internal Link Juicer API WordPress plugin's REST API.

The `internal-link-juicer-api-client` is a Unofficial Python library that simplifies interaction with the "Internal Link Juicer" WordPress plugin's via REST API.  This client empowers developers to automate and integrate keyword management tasks into their workflows.

**Key Features:**

*   **Easy-to-use API:**  Simple methods for common operations like `get_definitions()`, `update_definition_by_post_id()`, and `update_definition_by_meta_id()`.
*   **Pagination Support:**  Efficiently retrieve large numbers of keyword definitions using built-in pagination.
*   **Automatic Serialization:**  Handles the conversion of Python lists to the PHP serialized format required by the Internal Link Juicer plugin.
*   **Error Handling:**  Robust error handling with informative exceptions.
*   **Secure Authentication:** Uses WordPress Application Passwords for secure API access.

**Use Cases:**

*   **Bulk Keyword Updates:**  Modify keywords across multiple posts simultaneously.
*   **Automated Content Analysis:**  Integrate with content analysis tools to dynamically adjust keywords.
*   **Custom Dashboards:** Build custom dashboards and reporting tools that interact with Internal Link Juicer data.
*   **Data Migration:**  Easily transfer keyword definitions between WordPress sites.
*   **Testing and Development:**  Streamline the process of testing and developing Internal Link Juicer configurations.
*   **Data integration with 3rd Party tools:** Easily adapt/manipulate/correlate internal-link-juicer,  and inject your SEO strategy  seamlessly with your python code.

**Requires:**

*   Python 3.7+
*   `requests` library
*   `phpserialize` library
*   A WordPress installation with the `internal-link-juicer-api` plugin installed and activated.
