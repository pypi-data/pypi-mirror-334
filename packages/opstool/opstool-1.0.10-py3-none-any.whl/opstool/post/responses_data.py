from typing import Union
from types import SimpleNamespace

import numpy as np
import openseespy.opensees as ops
import xarray as xr

from ._get_response import (
    ModelInfoStepData,
    NodalRespStepData,
    TrussRespStepData,
    FrameRespStepData,
    LinkRespStepData,
    FiberSecRespStepData,
    ShellRespStepData,
    PlaneRespStepData,
    BrickRespStepData,
    ContactRespStepData
)
from .eigen_data import save_eigen_data
from .model_data import save_model_data
from ..utils import get_random_color, CONSTANTS


POST_ARGS = SimpleNamespace(
    elastic_frame_sec_points=7,
)


class CreateODB:
    """Create an output database (ODB) to save response data.

    Parameters
    ------------
    odb_tag: Union[int, str], default: 1
        Tag of output databases (ODB) to be saved.
    model_update: bool, default: False
        Whether to update the model data.

        .. Note::
            If True, the model data will be updated at each step.
            If no nodes and elements are added or removed during the analysis of your model,
            keep this parameter set to **False**.
            Enabling model updates unnecessarily can increase memory usage and slow down performance.
            If some nodes or elements are deleted during the analysis, you should set this parameter to `True`.

    save_nodal_resp: bool, default: True
        Whether to save nodal responses.
    save_frame_resp: bool, default: True
        Whether to save frame element responses.
    save_truss_resp: bool, default: True
        Whether to save truss element responses.
    save_link_resp: bool, default: True
        Whether to save link element responses.
    save_shell_resp: bool, default: True
        Whether to save shell element responses.
    save_fiber_sec_resp: bool, default: True
        Whether to save fiber section responses.
    save_plane_resp: bool, default: True
        Whether to save plane element responses.
    save_brick_resp: bool, default: True
        Whether to save brick element responses.
    save_contact_resp: bool, default: True
        Whether to save contact element responses.
    node_tags: Union[list, tuple, int], default: None
        Node tags to be saved.
        If None, save all nodes' responses.
    frame_tags: Union[list, tuple, int], default: None
        Frame element tags to be saved.
        If None, save all frame elements' responses.
    truss_tags: Union[list, tuple, int], default: None
        Truss element tags to be saved.
        If None, save all truss elements' responses.
    link_tags: Union[list, tuple, int], default: None
        Link element tags to be saved.
        If None, save all link elements' responses.
    shell_tags: Union[list, tuple, int], default: None
        Shell element tags to be saved.
        If None, save all shell elements' responses.
    plane_tags: Union[list, tuple, int], default: None
        Plane element tags to be saved.
        If None, save all plane elements' responses.
    brick_tags: Union[list, tuple, int], default: None
        Brick element tags to be saved.
        If None, save all brick elements' responses.
    contact_tags: Union[list, tuple, int], default: None
        Contact element tags to be saved.

    .. Note::
        If you enter optional node and element tags to avoid saving all data,
        make sure these tags are not deleted during the analysis.
        Otherwise, unexpected behavior may occur.

    kwargs: Other post-processing parameters, optional:
        * elastic_frame_sec_points: int, default: 7
            The number of elastic frame elements section points.
            A larger number may result in a larger file size.
    """

    def __init__(
            self,
            odb_tag: Union[int, str] = 1,
            model_update: bool = False,
            save_nodal_resp: bool = True,
            save_frame_resp: bool = True,
            save_truss_resp: bool = True,
            save_link_resp: bool = True,
            save_shell_resp: bool = True,
            save_fiber_sec_resp: bool = True,
            save_plane_resp: bool = True,
            save_brick_resp: bool = True,
            save_contact_resp: bool = True,
            node_tags: Union[list, tuple, int] = None,
            frame_tags: Union[list, tuple, int] = None,
            truss_tags: Union[list, tuple, int] = None,
            link_tags: Union[list, tuple, int] = None,
            shell_tags: Union[list, tuple, int] = None,
            plane_tags: Union[list, tuple, int] = None,
            brick_tags: Union[list, tuple, int] = None,
            contact_tags: Union[list, tuple, int] = None,
            **kwargs
    ):
        self.odb_tag = odb_tag
        self.model_update = model_update
        self.save_nodal_resp = save_nodal_resp
        self.save_frame_resp = save_frame_resp
        self.save_truss_resp = save_truss_resp
        self.save_link_resp = save_link_resp
        self.save_shell_resp = save_shell_resp
        self.save_fiber_sec_resp = save_fiber_sec_resp
        self.save_plane_resp = save_plane_resp
        self.save_brick_resp = save_brick_resp
        self.save_contact_resp = save_contact_resp

        self.node_tags = node_tags
        self.frame_tags = frame_tags
        self.truss_tags = truss_tags
        self.link_tags = link_tags
        self.shell_tags = shell_tags
        self.plane_tags = plane_tags
        self.brick_tags = brick_tags
        self.contact_tags = contact_tags

        if node_tags is not None:
            self.node_tags = [int(tag) for tag in np.atleast_1d(node_tags)]
        if frame_tags is not None:
            self.frame_tags = [int(tag) for tag in np.atleast_1d(frame_tags)]
        if truss_tags is not None:
            self.truss_tags = [int(tag) for tag in np.atleast_1d(truss_tags)]
        if link_tags is not None:
            self.link_tags = [int(tag) for tag in np.atleast_1d(link_tags)]
        if shell_tags is not None:
            self.shell_tags = [int(tag) for tag in np.atleast_1d(shell_tags)]
        if plane_tags is not None:
            self.plane_tags = [int(tag) for tag in np.atleast_1d(plane_tags)]
        if brick_tags is not None:
            self.brick_tags = [int(tag) for tag in np.atleast_1d(brick_tags)]
        if contact_tags is not None:
            self.contact_tags = [int(tag) for tag in np.atleast_1d(contact_tags)]

        self.ModelInfo = None
        self.NodalResp = None
        self.FrameResp = None
        self.TrussResp = None
        self.LinkResp = None
        self.ShellResp = None
        self.FiberSecResp = None
        self.PlaneResp = None
        self.BrickResp = None
        self.ContactResp = None

        for key, value in kwargs.items():
            setattr(POST_ARGS, key, value)

        self.initialize()

    def _get_resp(self):
        output = [
            self.ModelInfo, self.NodalResp, self.FrameResp, self.TrussResp,
            self.LinkResp, self.ShellResp, self.FiberSecResp,
            self.PlaneResp, self.BrickResp, self.ContactResp,
        ]
        return output

    def initialize(self):
        self.ModelInfo = ModelInfoStepData(model_update=self.model_update)
        if self.node_tags is not None:
            node_tags = self.node_tags
        else:
            node_tags = self.ModelInfo.get_current_node_tags()
        if len(node_tags) > 0 and self.save_nodal_resp:
            self.NodalResp = NodalRespStepData(node_tags)
        # -----------------------------------------------------------------
        if self.frame_tags is not None:
            frame_tags = self.frame_tags
        else:
            frame_tags = self.ModelInfo.get_current_frame_tags()
        frame_load_data = self.ModelInfo.get_current_frame_load_data()
        if len(frame_tags) > 0 and self.save_frame_resp:
            self.FrameResp = FrameRespStepData(
                frame_tags,
                frame_load_data,
                elastic_frame_sec_points=POST_ARGS.elastic_frame_sec_points
            )
        # -----------------------------------------------------------------
        if self.truss_tags is not None:
            truss_tags = self.truss_tags
        else:
            truss_tags = self.ModelInfo.get_current_truss_tags()
        if len(truss_tags) > 0 and self.save_truss_resp:
            self.TrussResp = TrussRespStepData(truss_tags)
        # -----------------------------------------------------------------
        if self.link_tags is not None:
            link_tags = self.link_tags
        else:
            link_tags = self.ModelInfo.get_current_link_tags()
        if len(link_tags) > 0 and self.save_link_resp:
            self.LinkResp = LinkRespStepData(link_tags)
        # -----------------------------------------------------------------
        if self.shell_tags is not None:
            shell_tags = self.shell_tags
        else:
            shell_tags = self.ModelInfo.get_current_shell_tags()
        if len(shell_tags) > 0 and self.save_shell_resp:
            self.ShellResp = ShellRespStepData(shell_tags)
        # -----------------------------------------------------------------
        if self.save_fiber_sec_resp:
            self.FiberSecResp = FiberSecRespStepData()
        # -----------------------------------------------------------------
        if self.plane_tags is not None:
            plane_tags = self.plane_tags
        else:
            plane_tags = self.ModelInfo.get_current_plane_tags()
        if len(plane_tags) > 0 and self.save_plane_resp:
            self.PlaneResp = PlaneRespStepData(plane_tags)
        # -----------------------------------------------------------------
        if self.brick_tags is not None:
            brick_tags = self.brick_tags
        else:
            brick_tags = self.ModelInfo.get_current_brick_tags()
        if len(brick_tags) > 0 and self.save_brick_resp:
            self.BrickResp = BrickRespStepData(brick_tags)
        # -----------------------------------------------------------------
        if self.contact_tags is not None:
            contact_tags = self.contact_tags
        else:
            contact_tags = self.ModelInfo.get_current_contact_tags()
        if len(contact_tags) > 0 and self.save_contact_resp:
            self.ContactResp = ContactRespStepData(contact_tags)

    def reset(self):
        for resp in self._get_resp():
            if resp is not None:
                resp.reset()

    def fetch_response_step(self, print_info: bool = False):
        """Extract response data for the current moment.

        Parameters
        ------------
        print_info: bool, optional
            print information, by default, False
        """
        self.ModelInfo.add_data_one_step()
        if self.node_tags is not None:
            node_tags = self.node_tags
        else:
            node_tags = self.ModelInfo.get_current_node_tags()
        if len(node_tags) > 0 and self.save_nodal_resp:
            self.NodalResp.add_data_one_step(node_tags)
        # -----------------------------------------------------------------
        if self.frame_tags is not None:
            frame_tags = self.frame_tags
        else:
            frame_tags = self.ModelInfo.get_current_frame_tags()
        frame_load_data = self.ModelInfo.get_current_frame_load_data()
        if len(frame_tags) > 0 and self.save_frame_resp:
            self.FrameResp.add_data_one_step(frame_tags, frame_load_data)
        # -----------------------------------------------------------------
        if self.truss_tags is not None:
            truss_tags = self.truss_tags
        else:
            truss_tags = self.ModelInfo.get_current_truss_tags()
        if len(truss_tags) > 0 and self.save_truss_resp:
            self.TrussResp.add_data_one_step(truss_tags)
        # -----------------------------------------------------------------
        if self.link_tags is not None:
            link_tags = self.link_tags
        else:
            link_tags = self.ModelInfo.get_current_link_tags()
        if len(link_tags) > 0 and self.save_link_resp:
            self.LinkResp.add_data_one_step(link_tags)
        # -----------------------------------------------------------------
        if self.shell_tags is not None:
            shell_tags = self.shell_tags
        else:
            shell_tags = self.ModelInfo.get_current_shell_tags()
        if len(shell_tags) > 0 and self.save_shell_resp:
            self.ShellResp.add_data_one_step(shell_tags)
        if self.save_fiber_sec_resp:
            self.FiberSecResp.add_data_one_step()
        # -----------------------------------------------------------------
        if self.plane_tags is not None:
            plane_tags = self.plane_tags
        else:
            plane_tags = self.ModelInfo.get_current_plane_tags()
        # -----------------------------------------------------------------
        if len(plane_tags) > 0 and self.save_plane_resp:
            self.PlaneResp.add_data_one_step(plane_tags)
        # -----------------------------------------------------------------
        if self.brick_tags is not None:
            brick_tags = self.brick_tags
        else:
            brick_tags = self.ModelInfo.get_current_brick_tags()
        if len(brick_tags) > 0 and self.save_brick_resp:
            self.BrickResp.add_data_one_step(brick_tags)
        # -----------------------------------------------------------------
        if self.contact_tags is not None:
            contact_tags = self.contact_tags
        else:
            contact_tags = self.ModelInfo.get_current_contact_tags()
        if len(contact_tags) > 0 and self.save_contact_resp:
            self.ContactResp.add_data_one_step(contact_tags)

        if print_info:
            time = ops.getTime()
            CONSOLE = CONSTANTS.get_console()
            PKG_PREFIX = CONSTANTS.get_pkg_prefix()
            color = get_random_color()
            CONSOLE.print(
                f"{PKG_PREFIX} The responses data at time [bold {color}]{time:.4f}[/] has been fetched!"
            )

    def save_response(self, zlib: bool = False):
        """
        Save all response data to a file name ``RespStepData-{odb_tag}.nc``.

        Parameters
        -----------
        zlib: bool, optional, default: False
            If True, the data is saved compressed,
            which is useful when your result files are expected to be large,
            especially if model updating is turned on.
        """
        RESULTS_DIR = CONSTANTS.get_output_dir()
        CONSOLE = CONSTANTS.get_console()
        PKG_PREFIX = CONSTANTS.get_pkg_prefix()

        filename = f"{RESULTS_DIR}/" + f"RespStepData-{self.odb_tag}.nc"
        with xr.DataTree(name="RespStepData") as dt:
            for resp in self._get_resp():
                if resp is not None:
                    resp.save_file(dt)

            if zlib:
                encoding = {}
                for path, node in dt.items():
                    if path == "ModelInfo":
                        for key, value in node.items():
                            encoding[f"/{path}/{key}"] = {
                                key: {
                                    "_FillValue": -9999,
                                    "zlib": True,
                                    "complevel": 5,
                                    "dtype": "float32"
                                }
                            }
                    else:
                        for key, value in node.items():
                            encoding[f"/{path}"] = {
                                key: {
                                    "_FillValue": -9999,
                                    "zlib": True,
                                    "complevel": 5,
                                    "dtype": "float32"
                                }
                            }
            else:
                encoding = None

            dt.to_netcdf(filename, mode="w", engine="netcdf4", encoding=encoding)

        color = get_random_color()
        CONSOLE.print(
            f"{PKG_PREFIX} All responses data with odb_tag = {self.odb_tag} "
            f"saved in [bold {color}]{filename}[/]!"
        )

    def save_eigen_data(
            self,
            mode_tag: int = 1,
            solver: str = "-genBandArpack",
    ):
        """Save modal analysis data.

        Parameters
        ----------
        mode_tag : int, optional,
            Modal tag, all modal data smaller than this modal tag will be saved, by default 1
        solver : str, optional,
           OpenSees' eigenvalue analysis solver, by default "-genBandArpack".
        """
        save_eigen_data(odb_tag=self.odb_tag, mode_tag=mode_tag, solver=solver)

    def save_model_data(
            self,
    ):
        """Save the model data from the current domain."""
        save_model_data(odb_tag=self.odb_tag)


def loadODB(obd_tag, resp_type: str = "Nodal"):
    """Load saved response data.

    Parameters
    ----------

    Returns
    --------
    Relevant to a response type.
    """
    RESULTS_DIR = CONSTANTS.get_output_dir()
    CONSOLE = CONSTANTS.get_console()
    PKG_PREFIX = CONSTANTS.get_pkg_prefix()

    filename = f"{RESULTS_DIR}/" + f"RespStepData-{obd_tag}.nc"
    with xr.open_datatree(filename, engine="netcdf4").load() as dt:
        color = get_random_color()
        CONSOLE.print(
            f"{PKG_PREFIX} Loading response data from [bold {color}]{filename}[/] ..."
        )
        model_info_steps, model_update = ModelInfoStepData.read_file(dt)
        if resp_type.lower() == "nodal":
            resp_step = NodalRespStepData.read_file(dt)
        elif resp_type.lower() == "frame":
            resp_step = FrameRespStepData.read_file(dt)
        elif resp_type.lower() == "fibersec":
            resp_step = FiberSecRespStepData.read_file(dt)
        elif resp_type.lower() == "truss":
            resp_step = TrussRespStepData.read_file(dt)
        elif resp_type.lower() == "link":
            resp_step = LinkRespStepData.read_file(dt)
        elif resp_type.lower() == "shell":
            resp_step = ShellRespStepData.read_file(dt)
        elif resp_type.lower() == "plane":
            resp_step = PlaneRespStepData.read_file(dt)
        elif resp_type.lower() in ["brick", "solid"]:
            resp_step = BrickRespStepData.read_file(dt)
        elif resp_type.lower() == "contact":
            resp_step = ContactRespStepData.read_file(dt)
        else:
            raise ValueError(f"Unsupported response type {resp_type}!")

    return model_info_steps, model_update, resp_step


def get_model_data(
        odb_tag: int = None,
        data_type: str = "Nodal",
        from_responses: bool = False
):
    """Read model data from a file.

    Parameters
    ----------
    odb_tag: Union[int, str], default: one
        Tag of output databases (ODB) to be read.
    data_type: str, default: Nodal
        Type of data to be read.
        Optional: "Nodal"
    from_responses: bool, default: False
        Whether to read data from response data.
        If True, the data will be read from the response data file.
        This is useful when the model data is updated in an analysis process.

    Returns
    ---------
    ModelData: xarray.Dataset if model_update is True, otherwise xarray.DataArray
    """
    RESULTS_DIR = CONSTANTS.get_output_dir()
    CONSOLE = CONSTANTS.get_console()
    PKG_PREFIX = CONSTANTS.get_pkg_prefix()

    if data_type.lower() == "nodal":
        data_type = "NodalData"
    else:
        raise ValueError(f"Data type {data_type} not found.")
    if from_responses:
        filename = f"{RESULTS_DIR}/" + f"RespStepData-{odb_tag}.nc"
        with xr.open_datatree(filename, engine="netcdf4").load() as dt:
            data = ModelInfoStepData.read_data(dt, data_type)
    else:
        filename = f"{RESULTS_DIR}/" + f"ModelData-{odb_tag}.nc"
        with xr.open_datatree(filename, engine="netcdf4").load() as dt:
            data = dt["ModelInfo"][data_type][data_type]
    color = get_random_color()
    CONSOLE.print(
        f"{PKG_PREFIX} Loading {data_type} data from [bold {color}]{filename}[/] ..."
    )
    return data


def get_nodal_responses(
        odb_tag: int,
        resp_type: str = None,
        node_tags: Union[list, tuple, int] = None
) -> xr.Dataset:
    """Read nodal responses data from a file.

    Parameters
    ----------
    odb_tag: Union[int, str], default: one
        Tag of output databases (ODB) to be read.
    resp_type: str, default: disp
        Type of response to be read.
        Optional:

        * "disp" - Displacement at the node.
        * "vel" - Velocity at the node.
        * "accel" - Acceleration at the node.
        * "reaction" - Reaction forces at the node.
        * "reactionIncInertia" - Reaction forces including inertial effects.
        * "rayleighForces" - Forces resulting from Rayleigh damping.
        * "pressure" - Pressure applied to the node.
        * If None, return all responses.

        .. Note::
            If the nodes include fluid pressure dof,
            such as those used for ...UP elements, the pore pressure should be extracted using ``resp_type="vel"``,
            and the value is placed in the degree of freedom ``RZ``.

    node_tags: Union[list, tuple, int], default: None
        Node tags to be read.
        Such as [1, 2, 3] or numpy.array([1, 2, 3]) or 1.
        If None, return all nodal responses.

        .. Note::
            If some nodes are deleted during the analysis,
            their response data will be filled with `numpy.nan`.

    Returns
    ---------
    NodalResp: xarray.Dataset
        Nodal responses' data.

    .. Note::
        The returned data can be viewed using `.dims` and `.coords` to view the
        dimension names and coordinates.
        You can further index or process the data.

    """
    RESULTS_DIR = CONSTANTS.get_output_dir()
    CONSOLE = CONSTANTS.get_console()
    PKG_PREFIX = CONSTANTS.get_pkg_prefix()

    filename = f"{RESULTS_DIR}/" + f"RespStepData-{odb_tag}.nc"
    with xr.open_datatree(filename, engine="netcdf4").load() as dt:
        color = get_random_color()
        CONSOLE.print(
            f"{PKG_PREFIX} Loading {resp_type} response data from [bold {color}]{filename}[/] ..."
        )

        nodal_resp = NodalRespStepData.read_response(dt, resp_type=resp_type, node_tags=node_tags)
    return nodal_resp


def get_element_responses(
        odb_tag: int,
        ele_type: str,
        resp_type: str = None,
        ele_tags: Union[list, tuple, int] = None
) -> xr.Dataset:
    """Read nodal responses data from a file.

    Parameters
    ------------
    odb_tag: Union[int, str], default: one
        Tag of output databases (ODB) to be read.
    ele_type: str, default: Frame
        Type of element to be read.
        Optional: "Frame", "Truss", "Link", "Shell", "Plane", "Solid", "Contact
    resp_type: str, default: disp
        The response type, which depends on the parameter `ele_type`.
        If None, return all responses to that `ele_type`.

        #. For `Frame`:
            * "localForces": Local forces in the element local coordinate system.
            * "basicForces": Basic forces in the element basic coordinate system.
            * "basicDeformations": Basic deformations in the element basic coordinate system.
            * "plasticDeformation": Plastic deformations in the element basic coordinate system.
            * "sectionForces": Section forces in the element coordinate system.
            * "sectionDeformations": Section deformations in the element coordinate system.
            * "sectionLocs": Section locations, 0.0 to 1.0.
        #. For `Truss`:
            * "axialForce": Axial force.
            * "axialDefo": Axial deformation.
            * "Stress": Stress of material.
            * "Strain": Strain of material.
        #. For `Link`:
            * "basicDeformation": Basic deformation, i.e., pure deformation.
            * "basicForce": Basic force.
        #. For `Shell`:
            * "sectionForces": Sectional forces at Gauss points (per unit length).
            * "sectionDeformations": Sectional deformation at Gauss points (per unit length).
        #. For `Plane`:
            * "stresses": Stresses at Gauss points.
            * "strains": Strains at Gauss points.
        #. For `Brick` or 'Solid':
            * "stresses": Stresses at Gauss points.
            * "strains": Strains at Gauss points.
        #. For `Contact`:
            * "localForces": Local forces in the element local coordinate system (normal and tangential).
            * "localDisp": Local displacements in the element local coordinate system (normal and tangential).
            * "slips": Slips in the element local coordinate system (tangential).

    ele_tags: Union[list, tuple, int], default: None
        Element tags to be read.
        Such as [1, 2, 3] or numpy.array([1, 2, 3]) or 1.
        If None, return all nodal responses.

        .. note::
            If some nodes are deleted during the analysis,
            their response data will be filled with `numpy.nan`.

    Returns
    ---------
    EleResp: xarray.Dataset
        Element responses' data.

    .. note::
        The returned data can be viewed using `.dims`、`.coords` and `.attrs` to view the
        dimension names and coordinates.
        You can further index or process the data.
    """
    RESULTS_DIR = CONSTANTS.get_output_dir()
    CONSOLE = CONSTANTS.get_console()
    PKG_PREFIX = CONSTANTS.get_pkg_prefix()

    filename = f"{RESULTS_DIR}/" + f"RespStepData-{odb_tag}.nc"
    with xr.open_datatree(filename, engine="netcdf4").load() as dt:
        color = get_random_color()
        CONSOLE.print(
            f"{PKG_PREFIX} Loading {ele_type} {resp_type} response data from [bold {color}]{filename}[/] ..."
        )

        if ele_type.lower() == "frame":
            ele_resp = FrameRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
        elif ele_type.lower() == "truss":
            ele_resp = TrussRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
        elif ele_type.lower() == "link":
            ele_resp = LinkRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
        elif ele_type.lower() == "shell":
            ele_resp = ShellRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
        elif ele_type.lower() == "plane":
            ele_resp = PlaneRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
        elif ele_type.lower() in ["brick", "solid"]:
            ele_resp = BrickRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
        elif ele_type.lower() == "contact":
            ele_resp = ContactRespStepData.read_response(dt, resp_type=resp_type, ele_tags=ele_tags)
        else:
            raise ValueError(
                f"Unsupported element type {ele_type}, "
                "must in [Frame, Truss, Link, Shell, Plane, Solid]!"
            )

    return ele_resp
